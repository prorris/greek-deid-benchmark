#!/usr/bin/env python3
"""Score a Morpheus benchmark run against the arbitrated gold standard.

Implements the manuscript's Methods exactly:
  - Must-redact: identifier-level recall (primary) - an identifier is removed
    only if NO PART of it survives verbatim in the outgoing text (whole-word
    match; parts = whitespace-separated words). Word-level recall (secondary):
    proportion of identifier words removed. Whole-value survival also recorded
    (continuity with tools/deid_benchmark.py).
  - Over-redaction: share of must-survive probes NOT present verbatim in the
    outgoing text (destroyed or altered). clinical_reference counts as
    lab_value (user ruling).
  - Record-level prevalence: notes with >=1 identifier-level residual.
  - Egress coverage: share of leaked identifiers whose surviving part matches
    a flag the reviewer would see (kept flags; suppressed also reported).
  - Wilson 95% CIs; results by category and by specialty (cs/ca/ne).

Outputs next to the run file: <run>_decisions.json (every scored decision,
for the run-to-run reproducibility comparison) and <run>_summary.md.

Usage: python3 benchmark_score.py "Benchmark runs/run1_results.jsonl"
"""
import json, math, re, sys
from collections import defaultdict
from pathlib import Path

PACK = Path(__file__).resolve().parent.parent
run_path = Path(sys.argv[1])
if not run_path.is_absolute():
    run_path = PACK / run_path
    if not run_path.exists():          # results live in results/
        run_path = PACK / "results" / Path(sys.argv[1]).name

SPECIALTY = {"cs": "cardiac surgery", "ca": "cardiology", "ne": "nephrology"}
SURV_MAP = {"clinical_reference": "lab_value"}


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, centre - half) * 100, min(1.0, centre + half) * 100)


# Closed-class function words (articles, prepositions, conjunctions) - their
# presence anywhere in a note attributes nothing. Linguistic class, not a
# tuned list: no nouns/adjectives/names belong here.
_STOP = {"και", "του", "της", "των", "τον", "την", "το", "τα", "τη", "στο",
         "στη", "στα", "στις", "στον", "στην", "από", "προς", "για", "μετά",
         "κατά", "εντός", "επί", "μέχρι", "έως", "ως", "the", "of", "and",
         "for", "at", "in", "on"}
_YEAR = None  # set below


def scoreable(tok):
    """Can a surviving occurrence of this token be ATTRIBUTED to the identifier?

    The outgoing text is rewritten (surrogates + shifted dates), so scoring is
    by verbatim presence. Short numerics (house numbers, postcode halves,
    day-of-month) and date ordinals (1η, 2ας) appear naturally everywhere in
    clinical text - their presence cannot be attributed to a leak (the
    project's long-standing fragment-coincidence finding). Rule: a part is
    scoreable if it has >=3 letter/word characters, or is a numeric run of
    >=4 digits. Unscoreable parts still count through the whole-value check."""
    if re.fullmatch(r"\d+[^\W\d]{1,2}", tok, re.UNICODE):   # date ordinal 1η/2ας
        return False
    core = re.sub(r"[^\w]", "", tok, flags=re.UNICODE)
    if core.lower() in _STOP:
        return False
    if any(ch.isalpha() for ch in tok):
        return len(re.sub(r"[\W\d]", "", tok, flags=re.UNICODE)) >= 3
    return len(re.sub(r"\D", "", tok)) >= 4


def scoreable_in(tok, fine):
    """Category-aware attributability. Bare year tokens inside date/dob spans
    are unattributable: the pipeline SHIFTS dates (interval-preserving), so the
    outgoing text lawfully contains years near the original - a surviving
    '2023' is usually the shifted fake's year, not the original's (the known
    structure property of date shifting, stated in the manuscript). The
    whole-value check still catches an unshifted full date."""
    if fine in ("date", "dob") and re.fullmatch(r"\(?(19|20)\d\d\)?,?", tok):
        return False
    return scoreable(tok)


def present(value, haystack):
    """deid_benchmark._present: whole-word, case-insensitive, wrap-tolerant."""
    v = value.strip()
    if not v:
        return False
    left = r"(?<![A-Za-z0-9])" if v[0].isalnum() else ""
    right = r"(?![A-Za-z0-9])" if v[-1].isalnum() else ""
    body = r"\s+".join(re.escape(tok) for tok in v.split())
    return re.search(left + body + right, haystack, re.IGNORECASE) is not None


# ---- load ------------------------------------------------------------------
rows = [json.loads(l) for l in run_path.open(encoding="utf-8")]
header = rows[0]
footer = rows[-1] if rows[-1].get("type") == "footer" else None
egress = {r["id"]: r for r in rows if r.get("type") == "note"}
gold = json.load((PACK / "annotations" / "gold_standard.json").open(encoding="utf-8"))["notes"]
survive = defaultdict(list)
for line in (PACK / "corpus" / "deid_corpus_gemini500.jsonl").open(encoding="utf-8"):
    r = json.loads(line)
    for p in r["phi"]:
        if p.get("expect") == "survive":
            survive[r["id"]].append(p)

if set(egress) != set(gold):
    print(f"WARNING: partial run - scoring {len(egress)}/{len(gold)} notes")
    gold = {k: v for k, v in gold.items() if k in egress}
    survive = defaultdict(list, {k: v for k, v in survive.items() if k in egress})

# ---- score must-redact -----------------------------------------------------
id_tot = id_removed = 0
w_tot = w_removed = 0
bycat = defaultdict(lambda: [0, 0])       # fine -> [total, removed]
byspec = defaultdict(lambda: [0, 0])      # specialty -> [total, removed]
bycat_w = defaultdict(lambda: [0, 0])     # fine -> [words_total, words_removed]
leaks = []                                # identifier-level residuals
decisions = []
notes_with_leak = 0

for nid in sorted(gold):
    out = egress[nid]["egress"]
    spec = SPECIALTY[nid[:2]]
    note_leak = False
    for s in gold[nid]:
        parts = s["text"].split()
        sc_parts = [p for p in parts if scoreable_in(p, s["fine"])] or parts  # fall back: all-short value
        surviving = [p for p in sc_parts if present(p, out)]
        surviving_any = [p for p in parts if present(p, out)]   # literal-strict sensitivity
        whole = present(s["text"], out)
        removed = not surviving and not whole
        id_tot += 1
        w_tot += len(sc_parts)
        w_removed += len(sc_parts) - len(surviving)
        bycat[s["fine"]][0] += 1
        byspec[spec][0] += 1
        bycat_w[s["fine"]][0] += len(sc_parts)
        bycat_w[s["fine"]][1] += len(sc_parts) - len(surviving)
        if removed:
            id_removed += 1
            bycat[s["fine"]][1] += 1
            byspec[spec][1] += 1
        else:
            note_leak = True
            leaks.append({"note": nid, "fine": s["fine"], "value": s["text"],
                          "surviving": surviving or parts, "whole_value": whole})
        decisions.append({"note": nid, "start": s["start"], "end": s["end"],
                          "fine": s["fine"], "removed": removed,
                          "strict_all_parts_removed": not surviving_any,
                          "surviving": sorted(surviving)})
    if note_leak:
        notes_with_leak += 1

# ---- score must-survive ----------------------------------------------------
sv_tot = sv_kept = 0
sv_cat = defaultdict(lambda: [0, 0])
overred = []
for nid in sorted(survive):
    out = egress[nid]["egress"]
    for p in survive[nid]:
        cat = SURV_MAP.get(p["category"], p["category"])
        kept = present(p["value"], out)
        sv_tot += 1
        sv_cat[cat][0] += 1
        if kept:
            sv_kept += 1
            sv_cat[cat][1] += 1
        else:
            overred.append({"note": nid, "category": cat, "value": p["value"]})
        decisions.append({"note": nid, "survive": p["value"], "category": cat,
                          "kept": kept})

# ---- egress coverage of residual leaks -------------------------------------
def covered(part, flags):
    return any(present(part, fv) or present(fv, part) for _, fv in flags)

flagged = flagged_any = 0
for lk in leaks:
    kept_flags = [(c, v) for c, v, *_ in egress[lk["note"]]["flags"]]
    sup_flags = [(c, v) for c, v, *_ in egress[lk["note"]]["flags_suppressed"]]
    lk["flagged"] = any(covered(p, kept_flags) for p in lk["surviving"])
    lk["flagged_incl_suppressed"] = lk["flagged"] or any(
        covered(p, kept_flags + sup_flags) for p in lk["surviving"])
    flagged += lk["flagged"]
    flagged_any += lk["flagged_incl_suppressed"]

# ---- report ----------------------------------------------------------------
L = []
L.append(f"# Benchmark run: {run_path.name}")
L.append(f"Fingerprint {header.get('fingerprint')} (validated={header.get('fingerprint_validated')}), "
         f"self-test ok={header.get('selftest', {}).get('ok')}, started {header.get('started')}"
         + (f", total {footer['total_minutes']} min" if footer else "") + "\n")
lo, hi = wilson(id_removed, id_tot)
L.append("## Co-primary outcomes")
L.append(f"- **De-identification rate (identifier-level recall): "
         f"{100*id_removed/id_tot:.2f}%** ({id_removed}/{id_tot}; 95% CI {lo:.2f}-{hi:.2f}); "
         f"{id_tot-id_removed} residual identifiers")
lo, hi = wilson(sv_tot - sv_kept, sv_tot)
L.append(f"- **Over-redaction rate: {100*(sv_tot-sv_kept)/sv_tot:.2f}%** "
         f"({sv_tot-sv_kept}/{sv_tot} probes destroyed or altered; 95% CI {lo:.2f}-{hi:.2f})")
L.append(f"- Word-level recall (secondary): {100*w_removed/w_tot:.2f}% ({w_removed}/{w_tot} words)")
lo, hi = wilson(notes_with_leak, len(gold))
L.append(f"- Record-level prevalence: {100*notes_with_leak/len(gold):.2f}% "
         f"({notes_with_leak}/{len(gold)} notes with >=1 residual; 95% CI {lo:.2f}-{hi:.2f})")
if leaks:
    L.append(f"- **Egress-guard flag coverage: {flagged}/{len(leaks)} residual leaks flagged "
             f"({100*flagged/len(leaks):.1f}%)**; including suppressed flags {flagged_any}/{len(leaks)}")
else:
    L.append("- Egress-guard flag coverage: n/a (no residual leaks)")
strict_removed = sum(1 for d in decisions if d.get("strict_all_parts_removed"))
L.append(f"- Sensitivity (literal every-part rule, incl. unattributable short "
         f"numerics/day ordinals): {100*strict_removed/id_tot:.2f}% ({strict_removed}/{id_tot})")
L.append("\n*Scoring rule: an identifier is removed if neither its whole value nor any "
         "attributable part survives verbatim (whole-word match). Attributable part = "
         "word with >=3 letters or numeric run >=4 digits, excluding closed-class "
         "function words and, within date spans, bare year tokens (the interval-"
         "preserving date shift lawfully re-emits years). Everything excluded is still "
         "covered by the whole-value check.*")

L.append("\n## Recall by identifier category (identifier-level | word-level)")
L.append("| Category | Removed/Total | % | 95% CI | Word-level % |")
L.append("|---|---|---|---|---|")
for cat in sorted(bycat, key=lambda c: -bycat[c][0]):
    t, r = bycat[cat]
    wt, wr = bycat_w[cat]
    lo, hi = wilson(r, t)
    L.append(f"| {cat} | {r}/{t} | {100*r/t:.2f} | {lo:.1f}-{hi:.1f} | {100*wr/wt:.2f} |")

L.append("\n## Recall by specialty (identifier-level)")
L.append("| Specialty | Removed/Total | % | 95% CI |")
L.append("|---|---|---|---|")
for sp in sorted(byspec):
    t, r = byspec[sp]
    lo, hi = wilson(r, t)
    L.append(f"| {sp} | {r}/{t} | {100*r/t:.2f} | {lo:.1f}-{hi:.1f} |")

L.append("\n## Must-survive probes kept, by category")
L.append("| Category | Kept/Total | % |")
L.append("|---|---|---|")
for cat in sorted(sv_cat, key=lambda c: -sv_cat[c][0]):
    t, k = sv_cat[cat]
    L.append(f"| {cat} | {k}/{t} | {100*k/t:.2f} |")

if leaks:
    L.append(f"\n## Residual leaks ({len(leaks)}) - Table 4 material")
    L.append("| Note | Category | Gold value | Surviving part(s) | Whole value survived | Flagged |")
    L.append("|---|---|---|---|---|---|")
    for lk in leaks:
        L.append(f"| {lk['note']} | {lk['fine']} | {lk['value'][:40]} | "
                 f"{', '.join(lk['surviving'])[:40]} | {'yes' if lk['whole_value'] else 'no'} | "
                 f"{'YES' if lk['flagged'] else ('suppressed' if lk['flagged_incl_suppressed'] else 'no')} |")
if overred:
    L.append(f"\n## Over-redacted clinical probes ({len(overred)})")
    L.append("| Note | Category | Value |")
    L.append("|---|---|---|")
    for o in overred:
        L.append(f"| {o['note']} | {o['category']} | {o['value'][:60]} |")

base = run_path.with_suffix("")
(Path(str(base) + "_summary.md")).write_text("\n".join(L), encoding="utf-8")
json.dump({"run": run_path.name, "fingerprint": header.get("fingerprint"),
           "decisions": decisions},
          Path(str(base) + "_decisions.json").open("w", encoding="utf-8"),
          ensure_ascii=False)
print("\n".join(L[:20]))
print(f"\nwrote {base}_summary.md + _decisions.json")
