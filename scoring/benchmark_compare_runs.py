#!/usr/bin/env python3
"""Reproducibility endpoint: compare two benchmark runs decision-by-decision.

Compares the *_decisions.json of two runs: every scored decision (per-identifier
removed verdict + surviving parts, per-probe kept verdict) and the pipeline
fingerprints. Surrogate TEXT is expected to differ between runs (deliberate
security property); determinism is a property of the pipeline's DECISIONS.

Usage: python3 benchmark_compare_runs.py run1_decisions.json run2_decisions.json
"""
import json, sys
from pathlib import Path

a = json.load(open(sys.argv[1], encoding="utf-8"))
b = json.load(open(sys.argv[2], encoding="utf-8"))

print(f"fingerprints: {a['fingerprint']} vs {b['fingerprint']}"
      f" -> {'SAME' if a['fingerprint'] == b['fingerprint'] else 'DIFFERENT'}")


def key(d):
    if "survive" in d:
        return ("survive", d["note"], d["survive"], d["category"])
    return ("redact", d["note"], d["start"], d["end"], d["fine"])


da = {key(d): d for d in a["decisions"]}
db = {key(d): d for d in b["decisions"]}
assert set(da) == set(db), "decision sets differ in coverage"

diff = 0
for k in sorted(da):
    x, y = da[k], db[k]
    if "survive" in x:
        same = x["kept"] == y["kept"]
    else:
        same = (x["removed"] == y["removed"]
                and x["surviving"] == y["surviving"]
                and x.get("strict_all_parts_removed") == y.get("strict_all_parts_removed"))
    if not same:
        diff += 1
        if diff <= 20:
            print("DIFFERS:", k, "->", {kk: x[kk] for kk in x if kk not in ("note",)},
                  "vs", {kk: y[kk] for kk in y if kk not in ("note",)})

n = len(da)
print(f"\n{n - diff}/{n} scored decisions identical ({diff} differ)")
print("REPRODUCIBLE" if diff == 0 and a["fingerprint"] == b["fingerprint"]
      else "NOT fully reproducible - investigate before quoting")
