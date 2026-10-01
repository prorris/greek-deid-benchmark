#!/usr/bin/env python3
"""Build the arbitrated gold standard for the Morpheus benchmark.

Gold = (Reviewer A ∩ Reviewer B corrected spans)
       + arbitrated "redact" decisions (annotations/arbitration.json)
       + the user's 24 Aug 2026 consistency rulings (below)
       - bare-year marks, per the same rulings.

Consistency rulings (user, 24 Aug 2026, after arbitration):
  1. Bare calendar years ("το 2010", "2018") are NOT identifiers anywhere in
     the corpus - the 21 remaining pre-annotation marks of that shape are
     removed to match the arbitration outcome. Full dates and month(+year)
     mentions stay marked.
  2. Every occurrence of a ruled-redact place value is marked: adds the second
     "Ιεράπετρα" in cs12_avr_farmer and "ΓΝ Χανίων" in cs12_cabg_avr_fisherman
     (neither was pre-highlighted, so neither reviewer saw it marked).

Output: annotations/gold_standard.json
"""
import json, re
from pathlib import Path

PACK = Path(__file__).resolve().parent.parent
RP = PACK / "annotations"

corpus, order = {}, []
for line in (PACK / "corpus" / "deid_corpus_gemini500.jsonl").open(encoding="utf-8"):
    r = json.loads(line)
    corpus[r["id"]] = r["text"]
    order.append(r["id"])


def load(rev):
    out = {}
    for p in range(1, 6):
        d = json.load((RP / f"review_{rev}_page{p}.json").open(encoding="utf-8"))
        for nid, n in d["notes"].items():
            out[nid] = {(s["start"], s["end"], s["category"]) for s in n["spans"]}
    return out


A, B = load("A"), load("B")

# arbitration: one-sided spans the user ruled "redact"
add = set()
for x in json.load((RP / "arbitration.json").open(encoding="utf-8"))["decisions"]:
    if x["decision"] != "redact":
        continue
    src = A if x["kind"] == "a_only" else B
    cands = [s for s in src[x["note"]] if s[0] == x["lo"] and s[1] == x["hi"]]
    assert len(cands) == 1, (x, cands)
    add.add((x["note"],) + cands[0])

# ruling 2: the two never-highlighted occurrences of ruled-redact places
EXTRA = [("cs12_avr_farmer", "Ιεράπετρα", "address", 2),      # 2nd occurrence
         ("cs12_cabg_avr_fisherman", "ΓΝ Χανίων", "hospital", 1)]
for nid, value, cat, occurrence in EXTRA:
    ms = list(re.finditer(re.escape(value), corpus[nid]))
    m = ms[occurrence - 1]
    add.add((nid, m.start(), m.end(), cat))

BARE_YEAR = re.compile(r"\(?(το |τον )?(19|20)\d\d\)?$")

# fine (Table-1) categories: preset positions carry the corpus category;
# the 19 post-review additions are hand-classified (both names are patients')
CATMAP = {"hospital": "hospital", "address": "address", "greek_phone": "phone",
          "email": "other", "date": "date", "dob": "date", "amka": "id",
          "gr_id": "id", "greek_patient_name": "name", "greek_clinician": "name",
          "url": "hospital"}
ADD_FINE = {"name": "greek_patient_name", "address": "address",
            "hospital": "hospital", "date": "date"}

_corpus_recs = {}
for line in (PACK / "corpus" / "deid_corpus_gemini500.jsonl").open(encoding="utf-8"):
    r = json.loads(line)
    _corpus_recs[r["id"]] = r


def preset_fine(rec):
    text, seen, spans = rec["text"], set(), []
    for p in rec["phi"]:
        if p.get("expect") != "redact" or p["category"] not in CATMAP:
            continue
        for m in re.finditer(re.escape(p["value"]), text):
            k = (m.start(), m.end())
            if k not in seen:
                seen.add(k)
                spans.append({"start": m.start(), "end": m.end(),
                              "fine": p["category"]})
    spans.sort(key=lambda s: (s["start"], -(s["end"] - s["start"])))
    out, last = [], -1
    for s in spans:
        if s["start"] >= last:
            out.append(s)
            last = s["end"]
    return {(s["start"], s["end"]): s["fine"] for s in out}

gold = {}
dropped_years = 0
for nid in order:
    spans = A[nid] & B[nid]
    spans |= {(s, e, c) for (n, s, e, c) in add if n == nid}
    # ruling 1: bare years are not identifiers
    keep = set()
    for (s, e, c) in spans:
        if c == "date" and BARE_YEAR.fullmatch(corpus[nid][s:e]):
            dropped_years += 1
            continue
        keep.add((s, e, c))
    ss = sorted(keep)
    for i in range(1, len(ss)):
        assert ss[i][0] >= ss[i - 1][1], (nid, ss[i - 1], ss[i])
    pf = preset_fine(_corpus_recs[nid])
    gold[nid] = [{"start": s, "end": e, "category": c,
                  "fine": pf.get((s, e)) or ADD_FINE[c],
                  "text": corpus[nid][s:e]} for (s, e, c) in ss]

total = sum(len(v) for v in gold.values())
from collections import Counter
cats = Counter(s["category"] for v in gold.values() for s in v)
json.dump({"built": "2026-08-24",
           "method": "A∩B + arbitration.json redacts + 24 Aug consistency rulings"
                     " (bare years unmarked; 2 stray place occurrences added)",
           "corpus": "deid_corpus_gemini500.jsonl",
           "total_spans": total,
           "by_category": dict(cats.most_common()),
           "notes": gold},
          (RP / "gold_standard.json").open("w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(f"gold spans: {total}  (bare-year marks removed: {dropped_years})")
print("by category:", dict(cats.most_common()))
