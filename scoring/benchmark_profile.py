#!/usr/bin/env python3
"""Runtime-characteristics run for the Morpheus benchmark (secondary endpoint).

Same frozen pipeline and corpus as benchmark_run.py, but instruments timing
per stage FROM OUTSIDE (wrappers around module entry points - zero changes to
pipeline code) and records memory. Stages:
  presidio   - AnalyzerEngine.analyze (rule/spaCy recognition layers)
  clinical   - clinical_deid.redaction_spans (local clinical-NER pass)
  greek      - greek_deid.name_spans (Greek detection layer)
  deid_other - remainder of deidentify() (regex passes, gazetteers, HIPS, verify)
  tokeniser  - Tokeniser.tokenise_text
  guard      - egress_guard.scan_spans (+ planted_fakes.apply)
Memory: RSS after model load, RSS sampled after each note (ps), peak ru_maxrss.

Output JSONL: header (hardware, fingerprint), one row per note, footer.
Usage: venv/bin/python3 benchmark_profile.py <out.jsonl> [limit]
"""
import json, sys, time, os, resource, subprocess
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
from core import clinical_deid, greek_deid
import presidio_analyzer

acc = {}
def timed(module, name, key):
    orig = getattr(module, name)
    def wrap(*a, **k):
        t0 = time.perf_counter()
        try:
            return orig(*a, **k)
        finally:
            acc[key] = acc.get(key, 0.0) + (time.perf_counter() - t0)
    setattr(module, name, wrap)

timed(clinical_deid, "redaction_spans", "clinical")
timed(greek_deid, "name_spans", "greek")
timed(presidio_analyzer.AnalyzerEngine, "analyze", "presidio")

def rss_mb():
    out = subprocess.run(["ps", "-o", "rss=", "-p", str(os.getpid())],
                         capture_output=True, text=True).stdout.strip()
    return round(int(out) / 1024, 1) if out else None

out_path = Path(sys.argv[1])
limit = int(sys.argv[2]) if len(sys.argv) > 2 else None
notes = []
for line in (PACK / "corpus" / "deid_corpus_gemini500.jsonl").open(encoding="utf-8"):
    r = json.loads(line)
    notes.append((r["id"], r["text"]))
if limit:
    notes = notes[:limit]

t0 = time.time()
fp = pipeline_fingerprint.compute()
# warm-up on the first note so model load is excluded from per-note stages
_warm = {}
_ = deidentify(notes[0][1], bank=SurrogateBank(), status_out=_warm)
load_s = round(time.time() - t0, 1)
acc.clear()

hw = subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"],
                    capture_output=True, text=True).stdout.strip()
header = {"type": "header", "started": time.strftime("%Y-%m-%dT%H:%M:%S"),
          "fingerprint": fp.get("fingerprint"), "validated": fp.get("validated"),
          "hardware": f"MacBook Air, {hw}, 8 GB", "python": sys.version.split()[0],
          "model_load_plus_first_note_s": load_s, "rss_after_load_mb": rss_mb(),
          "notes": len(notes)}

with out_path.open("w", encoding="utf-8") as f:
    f.write(json.dumps(header, ensure_ascii=False) + "\n"); f.flush()
    t_run = time.time()
    for i, (nid, text) in enumerate(notes, 1):
        acc.clear()
        t_note = time.perf_counter()
        status = {}
        bank = SurrogateBank()
        clean, _n = deidentify(text, bank=bank, status_out=status)
        t_deid = time.perf_counter()
        tok = Tokeniser()
        planted = list(status.get("planted_fakes") or ())
        egress = tok.tokenise_text(clean, planted_out=planted)
        t_tok = time.perf_counter()
        raw = egress_guard.scan_spans(egress)
        planted_fakes.apply(raw, egress, records=planted,
                            values=set(tok._mrn_reverse.keys()) | set(bank.values()))
        t_guard = time.perf_counter()
        deid_total = t_deid - t_note
        staged = acc.get("presidio", 0) + acc.get("clinical", 0) + acc.get("greek", 0)
        row = {"type": "note", "id": nid, "words": len(text.split()),
               "total_s": round(t_guard - t_note, 3),
               "deid_s": round(deid_total, 3),
               "presidio_s": round(acc.get("presidio", 0), 3),
               "clinical_s": round(acc.get("clinical", 0), 3),
               "greek_s": round(acc.get("greek", 0), 3),
               "deid_other_s": round(max(0.0, deid_total - staged), 3),
               "tokeniser_s": round(t_tok - t_deid, 3),
               "guard_s": round(t_guard - t_tok, 3),
               "rss_mb": rss_mb()}
        f.write(json.dumps(row, ensure_ascii=False) + "\n"); f.flush()
        if i % 25 == 0:
            el = time.time() - t_run
            print(f"{i}/{len(notes)}  elapsed {el/60:.1f} min  "
                  f"eta {(el/i)*(len(notes)-i)/60:.1f} min", flush=True)
    peak_mb = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024*1024), 1)
    f.write(json.dumps({"type": "footer",
                        "finished": time.strftime("%Y-%m-%dT%H:%M:%S"),
                        "total_minutes": round((time.time() - t_run) / 60, 1),
                        "peak_rss_mb": peak_mb}, ensure_ascii=False) + "\n")
print("DONE", flush=True)
sys.stdout.flush(); sys.stderr.flush()
os._exit(0)
