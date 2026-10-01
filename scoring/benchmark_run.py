#!/usr/bin/env python3
"""Morpheus benchmark run over the 500-note Gemini corpus.

Mirrors the app's production egress path exactly (core/ai_extractor.py):
    status = {}; clean, _ = deidentify(text, bank=SurrogateBank(), status_out=status)
    out = Tokeniser().tokenise_text(clean, planted_out=planted)
    raw = egress_guard.scan_spans(out)
    found, suppressed = planted_fakes.apply(raw, out, records=planted, values=allowed)

One JSONL row per note: id, egress text, egress flags (shown + suppressed +
raw count), wall time. A header row records the pipeline fingerprint,
validation verdict, self-test result and library versions - the manuscript's
reproducibility endpoint compares runs on scored decisions AND fingerprints.

Usage: venv/bin/python3 benchmark_run.py <out.jsonl>   (run from the repo root)
"""
import json, sys, time, os
from pathlib import Path

# This script drove the proprietary Morpheus engine and is included for
# transparency: it shows exactly how the published results were produced.
# It cannot be run without the (non-public) engine source. Point MORPHEUS_REPO
# at an engine checkout to reproduce a run; all SCORING of the published
# results needs only the self-contained scripts in this folder.
REPO = Path(os.environ.get("MORPHEUS_REPO", "."))
PACK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

os.environ.setdefault("PYTHONHASHSEED", "0")
from core.determinism import ensure_hash_seed
ensure_hash_seed()

from core.deidentifier import deidentify
from core.surrogates import SurrogateBank
from core.tokeniser import Tokeniser
from core import egress_guard, planted_fakes, pipeline_fingerprint
from core import deid_selftest

out_path = Path(sys.argv[1])
limit = int(sys.argv[2]) if len(sys.argv) > 2 else None   # smoke-test aid
notes = []
for line in (PACK / "corpus" / "deid_corpus_gemini500.jsonl").open(encoding="utf-8"):
    r = json.loads(line)
    notes.append((r["id"], r["text"]))
if limit:
    notes = notes[:limit]

selftest = deid_selftest.run()
fp = pipeline_fingerprint.compute()
header = {"type": "header",
          "started": time.strftime("%Y-%m-%dT%H:%M:%S"),
          "corpus": "deid_corpus_gemini500.jsonl",
          "notes": len(notes),
          "fingerprint": fp.get("fingerprint"),
          "fingerprint_validated": fp.get("validated"),
          "selftest": {k: v for k, v in selftest.items()
                       if isinstance(v, (bool, str, int, float))}}

with out_path.open("w", encoding="utf-8") as f:
    f.write(json.dumps(header, ensure_ascii=False) + "\n")
    f.flush()
    t_run = time.time()
    for i, (nid, text) in enumerate(notes, 1):
        t0 = time.time()
        status = {}
        bank = SurrogateBank()
        clean, _ = deidentify(text, bank=bank, status_out=status)
        tok = Tokeniser()
        planted = list(status.get("planted_fakes") or ())
        egress = tok.tokenise_text(clean, planted_out=planted)
        allowed = set(tok._mrn_reverse.keys()) | set(bank.values())
        raw = egress_guard.scan_spans(egress)
        found, suppressed = planted_fakes.apply(raw, egress,
                                                records=planted, values=allowed)
        row = {"type": "note", "id": nid, "seconds": round(time.time() - t0, 2),
               "egress": egress,
               "flags": [list(x) for x in found],
               "flags_suppressed": [list(x) for x in suppressed],
               "flags_raw_n": len(raw)}
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
        f.flush()
        if i % 25 == 0:
            el = time.time() - t_run
            print(f"{i}/{len(notes)}  elapsed {el/60:.1f} min  "
                  f"eta {(el/i)*(len(notes)-i)/60:.1f} min", flush=True)
    f.write(json.dumps({"type": "footer",
                        "finished": time.strftime("%Y-%m-%dT%H:%M:%S"),
                        "total_minutes": round((time.time() - t_run) / 60, 1)},
                       ensure_ascii=False) + "\n")
print("DONE", flush=True)
sys.stdout.flush(); sys.stderr.flush()
os._exit(0)  # skip sentencepiece/abseil teardown SIGBUS (known, harmless)
