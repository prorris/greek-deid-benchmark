#!/usr/bin/env python3
"""Inter-annotator agreement + disagreement list for the dual full review.

Inputs:  annotations/review_A_page{1..5}.json, review_B_page{1..5}.json
         deid_corpus_gemini500.jsonl (note texts; span offsets anchor to it)
Outputs: annotations/iaa_report.md          (human-readable summary)
         annotations/disagreements.json    (machine-readable, feeds the
                                             arbitration page builder)

Matching rules (identifier-level, mirroring the manuscript's primary metric):
  - exact agreement   : same (start, end) and same category in both sets
  - category conflict : same (start, end), different category
  - boundary conflict : overlapping spans, boundaries differ (greedy max-
                        overlap pairing after exact matches are removed)
  - A-only / B-only   : span with no overlap in the other set

IAA is reported as positive (pairwise) agreement F1 = 2M / (|A|+|B|) at two
granularities: strict (exact span + category) and relaxed (any overlap).
Cohen's kappa is not computed - there is no defined negative class for span
annotation (i2b2 convention).
"""
import json, re
from pathlib import Path
from collections import Counter, defaultdict

PACK = Path(__file__).resolve().parent.parent
RP = PACK / "annotations"

corpus = {}
for line in (PACK / "corpus" / "deid_corpus_gemini500.jsonl").open(encoding="utf-8"):
    r = json.loads(line)
    corpus[r["id"]] = r["text"]


def load(rev):
    notes = {}
    for p in range(1, 6):
        d = json.load((RP / f"review_{rev}_page{p}.json").open(encoding="utf-8"))
        for nid, n in d["notes"].items():
            spans = [dict(s) for s in n["spans"]]
            spans.sort(key=lambda s: (s["start"], s["end"]))
            notes[nid] = spans
    return notes


A, B = load("A"), load("B")
assert set(A) == set(B) == set(corpus)


# The original pre-annotations, rebuilt with the same logic as the pages,
# so each disagreement can say what the preset was.
CATMAP_SRC = (PACK / "tools" / "build_review_pages.py").read_text(encoding="utf-8")


def preset_spans(rec_text, phi, catmap):
    seen, spans = set(), []
    for p in phi:
        cat = catmap.get(p.get("category", ""), p.get("category", "other"))
        for m in re.finditer(re.escape(p["value"]), rec_text):
            key = (m.start(), m.end())
            if key in seen:
                continue
            seen.add(key)
            spans.append({"start": m.start(), "end": m.end(),
                          "text": m.group(0), "category": cat})
    spans.sort(key=lambda s: (s["start"], -(s["end"] - s["start"])))
    out, last_end = [], -1
    for s in spans:
        if s["start"] >= last_end:
            out.append(s)
            last_end = s["end"]
    return out


def overlap(a, b):
    return max(0, min(a["end"], b["end"]) - max(a["start"], b["start"]))


def match_note(sa, sb):
    """Return (exact, catconf, boundary, a_only, b_only) lists of pairs/spans."""
    sa, sb = list(sa), list(sb)
    exact, catconf, boundary = [], [], []
    used_a, used_b = set(), set()
    bykey_b = defaultdict(list)
    for j, s in enumerate(sb):
        bykey_b[(s["start"], s["end"])].append(j)
    for i, s in enumerate(sa):
        for j in bykey_b.get((s["start"], s["end"]), []):
            if j in used_b:
                continue
            used_a.add(i); used_b.add(j)
            (exact if s["category"] == sb[j]["category"] else catconf).append((s, sb[j]))
            break
    # greedy max-overlap pairing for the rest
    cands = []
    for i, s in enumerate(sa):
        if i in used_a:
            continue
        for j, t in enumerate(sb):
            if j in used_b:
                continue
            ov = overlap(s, t)
            if ov > 0:
                cands.append((ov, i, j))
    for ov, i, j in sorted(cands, key=lambda x: -x[0]):
        if i in used_a or j in used_b:
            continue
        used_a.add(i); used_b.add(j)
        boundary.append((sa[i], sb[j]))
    a_only = [s for i, s in enumerate(sa) if i not in used_a]
    b_only = [s for j, s in enumerate(sb) if j not in used_b]
    return exact, catconf, boundary, a_only, b_only


def ctx(text, start, end, pad=60):
    a, b = max(0, start - pad), min(len(text), end + pad)
    pre = ("…" if a > 0 else "") + text[a:start]
    post = text[end:b] + ("…" if b < len(text) else "")
    return pre.replace("\n", " "), post.replace("\n", " ")


tot = Counter()
percat_match = Counter()
percat_total = Counter()
disagreements = []
for nid in sorted(A):
    ex, cc, bd, ao, bo = match_note(A[nid], B[nid])
    tot["exact"] += len(ex); tot["catconf"] += len(cc)
    tot["boundary"] += len(bd); tot["a_only"] += len(ao); tot["b_only"] += len(bo)
    for s, t in ex:
        percat_match[s["category"]] += 2
    for spans, side in ((A[nid], "A"), (B[nid], "B")):
        for s in spans:
            percat_total[s["category"]] += 1
    text = corpus[nid]
    items = []
    for s, t in cc:
        items.append({"kind": "category", "a": s, "b": t})
    for s, t in bd:
        items.append({"kind": "boundary", "a": s, "b": t})
    for s in ao:
        items.append({"kind": "a_only", "a": s, "b": None})
    for s in bo:
        items.append({"kind": "b_only", "a": None, "b": s})
    for it in items:
        ref = it["a"] or it["b"]
        lo = min(x["start"] for x in (it["a"], it["b"]) if x)
        hi = max(x["end"] for x in (it["a"], it["b"]) if x)
        pre, post = ctx(text, lo, hi)
        it.update({"note": nid, "pre": pre, "post": post,
                   "lo": lo, "hi": hi, "mid": text[lo:hi]})
        disagreements.append(it)

nA = sum(len(v) for v in A.values())
nB = sum(len(v) for v in B.values())
strict_M = tot["exact"]
relax_M = tot["exact"] + tot["catconf"] + tot["boundary"]
strict_f1 = 2 * strict_M / (nA + nB)
relax_f1 = 2 * relax_M / (nA + nB)
cat_agree = tot["exact"] / (tot["exact"] + tot["catconf"]) if (tot["exact"] + tot["catconf"]) else 1.0

notes_with_dis = sorted({d["note"] for d in disagreements})

lines = []
lines.append("# Inter-annotator agreement — dual full review (pre-arbitration)\n")
lines.append(f"Reviewer A spans: **{nA}**  ·  Reviewer B spans: **{nB}**  ·  notes: 500 (both complete)\n")
lines.append("| Measure | Value |")
lines.append("|---|---|")
lines.append(f"| Strict agreement F1 (exact span + category) | **{strict_f1:.4f}** |")
lines.append(f"| Relaxed agreement F1 (any overlap) | **{relax_f1:.4f}** |")
lines.append(f"| Category agreement on identical spans | {cat_agree:.4f} |")
lines.append(f"| Exact matches | {tot['exact']} |")
lines.append(f"| Category conflicts (same span) | {tot['catconf']} |")
lines.append(f"| Boundary conflicts (overlap) | {tot['boundary']} |")
lines.append(f"| A-only spans | {tot['a_only']} |")
lines.append(f"| B-only spans | {tot['b_only']} |")
lines.append(f"| Total disagreements to arbitrate | **{len(disagreements)}** |")
lines.append(f"| Notes containing at least one disagreement | {len(notes_with_dis)} / 500 |")
lines.append("")
lines.append("## Disagreements by kind and category\n")
kindcat = Counter((d["kind"], (d["a"] or d["b"])["category"]) for d in disagreements)
lines.append("| Kind | Category | Count |")
lines.append("|---|---|---|")
for (k, c), n in sorted(kindcat.items(), key=lambda x: -x[1]):
    lines.append(f"| {k} | {c} | {n} |")
lines.append("")
(RP / "iaa_report.md").write_text("\n".join(lines), encoding="utf-8")
json.dump({"generated_from": ["review_A_page1-5.json", "review_B_page1-5.json"],
           "corpus": "deid_corpus_gemini500.jsonl",
           "stats": {"A_spans": nA, "B_spans": nB, **tot,
                     "strict_f1": strict_f1, "relaxed_f1": relax_f1},
           "disagreements": disagreements},
          (RP / "disagreements.json").open("w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(f"strict F1 {strict_f1:.4f}  relaxed F1 {relax_f1:.4f}")
print(f"disagreements {len(disagreements)} in {len(notes_with_dis)} notes")
print("wrote iaa_report.md + disagreements.json")
