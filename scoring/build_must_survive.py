#!/usr/bin/env python3
"""Write annotations/must_survive.json from the corpus file.

The must-survive clinical probes live inside the corpus JSONL: every `phi`
entry whose `expect` is "survive". This script only collects them into one
file beside the must-redact gold standard, so that they are easy to find.
It adds nothing and changes nothing; the corpus file remains the source.

A probe is a category and a text value. It has no character offsets: the
scorer asks whether the value still stands verbatim in the outgoing text.

    python3 scoring/build_must_survive.py
"""
import collections
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "corpus" / "deid_corpus_gemini500.jsonl"
OUT = ROOT / "annotations" / "must_survive.json"
# benchmark_score.py reports this one category under lab_value.
SCORED_AS = {"clinical_reference": "lab_value"}

notes = {}
by_category = collections.Counter()
with CORPUS.open(encoding="utf-8") as fh:
    for line in fh:
        rec = json.loads(line)
        probes = [{"category": p["category"], "value": p["value"]}
                  for p in rec.get("phi", []) if p.get("expect") == "survive"]
        notes[rec["id"]] = probes
        for p in probes:
            by_category[SCORED_AS.get(p["category"], p["category"])] += 1

OUT.write_text(json.dumps({
    "source": CORPUS.name,
    "rule": 'every phi entry with expect == "survive"',
    "total_probes": sum(by_category.values()),
    "by_scored_category": dict(sorted(by_category.items(), key=lambda kv: -kv[1])),
    "scored_as": SCORED_AS,
    "notes": notes,
}, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"wrote {OUT.relative_to(ROOT)}: {sum(by_category.values())} probes in {len(notes)} notes")
