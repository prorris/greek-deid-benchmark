#!/usr/bin/env python3
"""Build the dual-review pages for the Gemini-500 corpus.

Reuses the study-grade annotator template (tools/build_annotation_page.py in
the app repo) and extends it into review mode:
  - every redact annotation PRE-HIGHLIGHTED (click removes, select adds);
  - machine-correction flags shown inline on the affected note;
  - 5 pages x 100 notes per reviewer, separate autosave keys and export names
    so Reviewer A (FPR) and Reviewer B (colleague) never collide.
Survive (clinical-content) probes are not part of this review by design.
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

PACK = Path(__file__).resolve().parent.parent
REPO = Path("/Users/prorris/Desktop/ClinicalMiner")
spec = importlib.util.spec_from_file_location(
    "bap", REPO / "tools" / "build_annotation_page.py")
bap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bap)
TEMPLATE = bap.HTML_TEMPLATE

CATMAP = {"hospital": "hospital", "address": "address", "greek_phone": "phone",
          "email": "other", "date": "date", "dob": "date", "amka": "id",
          "gr_id": "id", "greek_patient_name": "name", "greek_clinician": "name",
          "url": "hospital"}

recs = [json.loads(l) for l in
        (PACK / "deid_corpus_gemini500.jsonl").open(encoding="utf-8") if l.strip()]

def preset_spans(rec):
    text, seen, spans = rec["text"], set(), []
    for p in rec["phi"]:
        if p.get("expect") != "redact" or p["category"] not in CATMAP:
            continue
        cat = CATMAP[p["category"]]
        for m in re.finditer(re.escape(p["value"]), text):
            key = (m.start(), m.end())
            if key not in seen:
                seen.add(key)
                spans.append({"start": m.start(), "end": m.end(),
                              "text": m.group(0), "category": cat})
    # non-overlapping, longest-first
    spans.sort(key=lambda s: (s["start"], -(s["end"] - s["start"])))
    out, last_end = [], -1
    for s in spans:
        if s["start"] >= last_end:
            out.append(s); last_end = s["end"]
    for s in out:
        assert text[s["start"]:s["end"]] == s["text"]
    return out

# ---- flags: plain-language, identifier-relevant only ----------------------
flags: dict[str, list[str]] = {}
for line in (PACK / "REVIEW_NOTES.md").read_text(encoding="utf-8").splitlines():
    m = re.match(r"- ([a-z]{2}\d{2}_\w+): (.*)", line)
    if not m:
        continue
    nid, msg = m.groups()
    if "survive probe" in msg or "short note" in msg:
        continue  # not part of the identifier review
    if "repaired" in msg or "case-fixed" in msg:
        val = re.search(r"-> '([^']*)'", msg)
        text = ("An annotation here was auto-corrected"
                + (f" to «{val.group(1)}»" if val else "")
                + " — please confirm the highlight matches what you would mark.")
    elif "UNRESOLVED" in msg or "REDACT PROBE" in msg:
        text = ("One identifier annotation here could not be matched to the text "
                "— please mark the correct value yourself.")
    else:
        text = "Please double-check this note: " + msg
    flags.setdefault(nid, []).append(text)

# ---- page slices ----------------------------------------------------------
PAGES = [("1", "Cardiac surgery I (notes 1–100)", recs[0:100]),
         ("2", "Cardiac surgery II (notes 101–200)", recs[100:200]),
         ("3", "Cardiac surgery III (notes 201–300)", recs[200:300]),
         ("4", "Cardiology (100 notes)", recs[300:400]),
         ("5", "Nephrology (100 notes)", recs[400:500])]
REVIEWERS = [("A", "Reviewer A"), ("B", "Reviewer B")]

FLAG_CSS = ("#flagBox { display:none; background:#fff3cd; border:1px solid "
            "#e0c469; border-radius:8px; padding:8px 12px; margin:8px 0; "
            "font-size:14px; }\n</style>")

outdir = PACK / "Review pages"
for rev_key, rev_label in REVIEWERS:
    d = outdir / f"{rev_label}"
    d.mkdir(parents=True, exist_ok=True)
    for pno, ptitle, chunk in PAGES:
        notes = [{"id": r["id"], "text": r["text"]} for r in chunk]
        preset = {r["id"]: preset_spans(r) for r in chunk}
        pflags = {r["id"]: flags[r["id"]] for r in chunk if r["id"] in flags}
        page_title = f"{rev_label} — page {pno} of 5 · {ptitle}"

        html = TEMPLATE
        html = html.replace("<title>Note annotation — mark the identifiers</title>",
                            f"<title>{page_title}</title>")
        html = re.sub(r"<h1>[^<]*</h1>",
                      f"<h1>{page_title} — review &amp; correct the highlights</h1>",
                      html, count=1)
        html = re.sub(
            r"<b>How it works\.</b>.*?press",
            "<b>How this review works.</b> Every identifier the machine believes "
            "it found is <b>already highlighted</b>. Read the note as you would a "
            "real discharge letter and correct the highlights: <b>click a wrong "
            "highlight to remove it</b>; <b>select any missed identifier</b> "
            "(names, numbers, dates, phones, addresses — the patient's or their "
            "family's) and pick a category from the little menu. Trust your own "
            "judgement, not the machine's. A yellow box above a note means "
            "something specific needs your confirmation there. When a note is "
            "finished, tick <i>Done</i> — every note needs a tick. Your work "
            "saves itself in this browser; you can close the page and continue "
            "later. When all 100 are done, press",
            html, count=1, flags=re.S)
        html = html.replace(
            "Selected notes are starred \u2605 \u2014 but annotate as many as you like.",
            "Review every note on this page \u2014 the counter above tracks your progress.")
        html = html.replace("</style>", FLAG_CSS, 1)
        html = html.replace('<h2 id="noteTitle"></h2>',
                            '<h2 id="noteTitle"></h2>\n    <div id="flagBox"></div>')
        html = html.replace('const STORE_KEY = "deid_user_annotations_batch100_v1";',
                            f'const STORE_KEY = "gemini500_review_{rev_key}_p{pno}_v1";')
        html = html.replace(
            "state.spans = state.spans || {}; state.done = state.done || {};",
            "state.spans = state.spans || {}; state.done = state.done || {};\n"
            "const PRESET = __PRESET_JSON__;\n"
            "const FLAGS = __FLAGS_JSON__;\n"
            "for (const id in PRESET) if (!(id in state.spans)) "
            "state.spans[id] = PRESET[id].map(s => Object.assign({}, s));")
        html = html.replace('$("noteTitle").textContent = note.id;',
            '$("noteTitle").textContent = note.id;\n'
            '  const fb = $("flagBox"); const fl = FLAGS[note.id] || [];\n'
            '  if (fl.length) { fb.style.display = "block";\n'
            '    fb.innerHTML = fl.map(t => "\\u26a0 " + t).join("<br>"); }\n'
            '  else { fb.style.display = "none"; }')
        html = html.replace('corpus: "deid_corpus_batch100.jsonl",',
                            'corpus: "deid_corpus_gemini500.jsonl",')
        html = html.replace('a.download = "user_annotations.json";',
                            f'a.download = "review_{rev_key}_page{pno}.json";')
        html = html.replace("__NOTES_JSON__", json.dumps(notes, ensure_ascii=False))
        html = html.replace("__SUGGESTED_JSON__", "[]")
        html = html.replace("__PRESET_JSON__", json.dumps(preset, ensure_ascii=False))
        html = html.replace("__FLAGS_JSON__", json.dumps(pflags, ensure_ascii=False))
        assert "__" + "NOTES_JSON" + "__" not in html
        assert "__PRESET_JSON__" not in html and "__FLAGS_JSON__" not in html

        out = d / f"Page {pno} of 5 — {ptitle.split(' (')[0]}.html"
        out.write_text(html, encoding="utf-8")
        print(f"{out.name}  [{rev_label}]  notes={len(notes)}  "
              f"pre-highlights={sum(len(v) for v in preset.values())}  "
              f"flagged-notes={len(pflags)}")
print("done")
