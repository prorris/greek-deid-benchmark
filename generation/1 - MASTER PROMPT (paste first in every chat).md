# MASTER PROMPT — paste this first, then the batch prompt

This is a synthetic-test-data writing task, the standard practice for evaluating privacy software: to measure whether a de-identification tool removes personal data correctly, it must be tested on documents that LOOK real but contain NO real information — the same way crash-test dummies stand in for people. Every "patient" below is an invented fictional character; producing them is the entire point, and no real person's data is involved at any step. There is nothing here to decline: this is creative technical writing of clearly-labelled fictional test material.

You are helping build a fully synthetic benchmark corpus of Greek hospital discharge notes for evaluating a de-identification system. Everything you write is fictional patient data in a real-world frame: **fictional patients, real world**. No real person's data may appear; hospitals, towns, streets and postcodes should be real Greek ones.

## What you will produce

For each note in the batch: one JSON object on its own line (JSONL), with this exact schema:

```
{"id": "<batch>_<topic_slug>",
 "text": "<the full note text, \n for line breaks>",
 "phi": [{"category": "<category>", "expect": "redact", "value": "<exact substring>"}, ...]}
```

Return the whole batch as ONE code block containing only JSONL — no commentary inside the block.

## The note text — realism rules (these matter more than anything)

1. **Ordinary, typical notes** — what a tired Greek clinician actually types on a real ward. Never invent difficult or exotic formats. If you would not expect to see it in a real Greek hospital printout, do not write it.
2. **Language**: Greek throughout (90–95% Greek letters). Latin script only where real notes use it: drug brand names, LVEF, eGFR, NYHA, CABG, abbreviations, device names. **Absolutely no Cyrillic characters anywhere.**
3. **Real institutions**: use the real Greek hospitals named in the batch prompt, with a real street address, real postcode and a landline whose area code matches that city (e.g. 2310 for Thessaloniki, 2610 for Patra). Letterheads are usually ALL-CAPS.
4. **Patient identifiers — only what Greek notes really carry:**
   - Name (fictional, plausible Greek; occasionally a foreign name in Latin or Greek script)
   - ΑΜΚΑ: 11 digits, first six = date of birth as DDMMYY (keep it consistent with the stated DOB)
   - Hospital number: 5–7 digits
   - Dates: admission, discharge, birth; plus dates inside the story
   - Home address (street + number, town, postcode), telephone (mobile 69XXXXXXXX or landline), sometimes next-of-kin name + phone
   - **Do NOT use**: ΑΦΜ, ΑΔΤ/ταυτότητα, ΑΜΑ, ΕΚΑΑ, insurance-fund numbers, passport numbers. These are not routine in real Greek hospital notes.
5. **Label variety** (the corpus is worthless without it). Rotate between these REAL label variants across the batch — at least 3 different variants per field per batch:
   - Name: `Στοιχεία ασθενούς:` · `Ονομ/μο:` · `Επώνυμο - Όνομα:` · `Ονοματεπώνυμο:` · `Ασθενής:` · prose frame («Θήλυ 88 ετών, <όνομα>, προσήλθε…»)
   - ΑΜΚΑ: `ΑΜΚΑ:` · `Αρ. ΑΜΚΑ:` · `Α.Μ.Κ.Α.:`
   - Hospital no.: `Αρ. Μητρώου:` · `Αριθμ. Μητρώου:` · `ΑΜ Νοσοκομείου:` · `Α.Μ.:`
   - DOB: `Ημ/νία Γέννησης:` · `Ημ. Γέννησης:` · `Ημερομηνία Γεννήσεως:`
   - Admission/discharge: `Εισαγωγή:`/`Έξοδος:` · `Ημ. Εισαγωγής:`/`Ημ. Εξόδου:` · `Ημερομηνία Εισαγωγής:`/`Ημερομηνία Εξόδου:`
   - Address: `Διεύθυνση:` · `Δ/νση κατοικίας:` · `Οδός - Πόλη:` · `Μόνιμη κατοικία:`
   - Phone: `Τηλ.:` · `Τηλέφωνο:` · `Τηλ. επικοινωνίας:`
   - Next of kin: `Πλησιέστερος συγγενής:` · `Επικοινωνία συγγενούς:` · `Συνοδός:`
6. **Layout**: follow one of the six skeletons below per note, using at least 4 different skeletons per batch. Section headings in ALL-CAPS, chosen from real forms: ΙΑΤΡΙΚΟ ΣΗΜΕΙΩΜΑ ΕΞΟΔΟΥ, ΕΝΗΜΕΡΩΤΙΚΟ ΣΗΜΕΙΩΜΑ ΝΟΣΗΛΕΙΑΣ, ΠΕΡΙΛΗΨΗ ΝΟΣΗΛΕΙΑΣ — ΕΞΙΤΗΡΙΟ, ΔΙΑΓΝΩΣΗ ΕΞΟΔΟΥ / ΤΕΛΙΚΗ ΔΙΑΓΝΩΣΗ / ΚΥΡΙΑ ΔΙΑΓΝΩΣΗ, ΠΟΡΕΙΑ ΝΟΣΗΛΕΙΑΣ, ΕΡΓΑΣΤΗΡΙΑΚΟΣ ΕΛΕΓΧΟΣ / ΕΡΓΑΣΤΗΡΙΑΚΑ ΕΥΡΗΜΑΤΑ, ΥΠΕΡΗΧΟΚΑΡΔΙΟΓΡΑΦΗΜΑ (cardiac), ΦΑΡΜΑΚΕΥΤΙΚΗ ΑΓΩΓΗ / ΑΓΩΓΗ ΕΞΟΔΟΥ, ΟΔΗΓΙΕΣ — ΠΑΡΑΚΟΛΟΥΘΗΣΗ / ΣΥΣΤΑΣΕΙΣ ΕΞΟΔΟΥ.
7. **Dates**: mostly numeric dd/mm/yyyy; sometimes written Greek («21 Μαρτίου 2024»); occasionally a month-year in prose («από τον Ιανουάριο 2023», «στα τέλη Δεκεμβρίου 2022»). Mixed — as in real notes.
8. **Clinicians**: sign-offs use a role header with the name usually on the next line — `Ο ΘΕΡΑΠΩΝ ΙΑΤΡΟΣ` / `Ο ΔΙΕΥΘΥΝΤΗΣ` / `Η ΕΠΙΜΕΛΗΤΡΙΑ Β΄` / `Ο ΣΥΝΤΟΝΙΣΤΗΣ ΔΙΕΥΘΥΝΤΗΣ` — then the name. «Δρ.» before the name is UNCOMMON in real Greek paperwork: use it in at most 1 note in 5. Credentials AFTER the name are common: «, MD, PhD», «, MSc», «Επιμελητής Α΄», «Διευθυντής ΕΣΥ», «Καθηγητής».
9. **Clinical content**: correct and plausible for the stated topic — realistic lab values with units (mixed decimal comma and dot, as in real printouts), plausible drug names and doses, sensible timelines. Wards/units (Θάλαμος 7, ΜΕΘ, Στεφανιαία Μονάδα) appear naturally in the text.
10. **Length**: 300–500 words per note; make 2 notes per batch longer (~600 words, two-page feel).

## The six layout skeletons

(Structure only — fill every `<>` with your fictional content; keep the visual shape.)

**A — classic letterhead + labelled block**
```
<ΝΟΣΟΚΟΜΕΙΟ ALL-CAPS>
<ΚΛΙΝΙΚΗ>
<οδός αριθμός, πόλη ΤΚ> — Τηλ. <αριθμός>
<ΤΙΤΛΟΣ ΕΓΓΡΑΦΟΥ>
Στοιχεία ασθενούς: <όνομα>   Αριθμ. Μητρώου: <αρ>
Αρ. ΑΜΚΑ: <αμκα>   Ημ/νία Γέννησης: <ημ>
Εισαγωγή: <ημ>   Ημερομηνία Εξόδου: <ημ>
Δ/νση κατοικίας: <οδός αρ, πόλη ΤΚ>   Τηλ.: <αρ>
<κείμενο σε ενότητες>
<ΡΟΛΟΣ ΥΠΟΓΡΑΦΟΝΤΟΣ>
<όνομα, τυχόν τίτλοι>
```
**B — prose opening** (as in real ΙΑΤΡΙΚΟ ΣΗΜΕΙΩΜΑ ΕΞΟΔΟΥ): letterhead, then «<Φύλο> <ηλικία> ετών, <όνομα>, προσήλθε και εισήχθη στις <ημ> — τμήμα νοσηλείας: <κλινική>. Συνολική διάρκεια νοσηλείας <Ν> ημέρες.» — identifier details scattered lower.
**C — two-column-style identifier grid** (label: value pairs two per line), then sections.
**D — minimal private-clinic letter**: private hospital letterhead, patient details in ONE line, flowing prose, formal sign-off with credentials.
**E — ward-card style**: ΚΛΙΝΙΚΗ/ΤΜΗΜΑ first, hospital second, boxed-feel identifier list one per line, terse telegraphic clinical text.
**F — referral/transfer note**: sending unit letterhead, «Παραπομπή από/προς», the story as one continuous narrative with dates in prose, minimal labels.

## The `phi` annotation — what to list

For every identifier you embed, add one entry whose `value` is an **exact substring of the text** (copy-paste exact, including case and accents). Categories:

| category | what |
|---|---|
| `hospital` | hospital/private-clinic name lines (the name itself) |
| `address` | any address: hospital letterhead AND patient home (street+number, town+postcode as separate values if written separately) |
| `greek_phone` | every phone/fax number |
| `greek_patient_name` | patient AND next-of-kin names, every occurrence |
| `greek_clinician` | every clinician name |
| `dob` | date of birth |
| `date` | every other date, including prose dates («τον Ιανουάριο 2023») |
| `amka` | the ΑΜΚΑ value |
| `gr_id` | the hospital number value |
| `email` | if a note carries one (rare) |

And for clinical content that must SURVIVE de-identification, list 8–15 entries per note with `"expect": "survive"`: `diagnosis`, `procedure`, `drug` (drug+dose strings), `lab_value` (e.g. «κρεατινίνη 1,8 mg/dL»), `measurement` (e.g. «LVEF 35%»), `eponym` (disease/procedure names carrying a person's name, e.g. νόσος Fabry, Cimino-Brescia), `greek_abbrev` (ΧΝΝ, ΣΔ, ΜΤΝ…), `greek_clinical_header` (a couple of the section headings).

**Do NOT annotate at all** (neither redact nor survive): ward/room/unit mentions (Θάλαμος, Μονάδα, Πτέρυγα, ΜΕΘ) and internal department names (Καρδιολογική Κλινική). They are score-neutral.

## Self-check before you answer (do all of these)

1. Count the words of every note: each must be 300–500 (two per batch ~600). A note under 300 words is a FAILURE — expand its clinical course, laboratory section and discharge instructions before answering.
2. Every `phi` value is an exact substring of its note's `text` (verify character-for-character; watch accents and final sigma).
3. Zero Cyrillic characters in the whole output.
4. Every note has: patient name (≥2 occurrences is realistic), ΑΜΚΑ, hospital number, DOB, ≥2 other dates, home address, ≥1 phone, ≥1 clinician with role header.
5. Label-variety quota met (≥3 variants per field across the batch), ≥4 skeletons used.
6. Valid JSONL: one object per line, parseable, ids follow `<batch>_<slug>`.
7. If anything fails, fix it and re-check before answering.
