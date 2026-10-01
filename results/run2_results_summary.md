# Benchmark run: run2_results.jsonl
Fingerprint 765328fbf1241ea4 (validated=True), self-test ok=True, started 2026-08-24T16:50:21, total 27.6 min

## Co-primary outcomes
- **De-identification rate (identifier-level recall): 96.60%** (7667/7937; 95% CI 96.18-96.98); 270 residual identifiers
- **Over-redaction rate: 2.82%** (190/6747 probes destroyed or altered; 95% CI 2.45-3.24)
- Word-level recall (secondary): 96.72% (11364/11749 words)
- Record-level prevalence: 42.40% (212/500 notes with >=1 residual; 95% CI 38.14-46.77)
- **Egress-guard flag coverage: 2/270 residual leaks flagged (0.7%)**; including suppressed flags 2/270
- Sensitivity (literal every-part rule, incl. unattributable short numerics/day ordinals): 89.97% (7141/7937)

*Scoring rule: an identifier is removed if neither its whole value nor any attributable part survives verbatim (whole-word match). Attributable part = word with >=3 letters or numeric run >=4 digits, excluding closed-class function words and, within date spans, bare year tokens (the interval-preserving date shift lawfully re-emits years). Everything excluded is still covered by the whole-value check.*

## Recall by identifier category (identifier-level | word-level)
| Category | Removed/Total | % | 95% CI | Word-level % |
|---|---|---|---|---|
| date | 1633/1686 | 96.86 | 95.9-97.6 | 96.64 |
| address | 1582/1655 | 95.59 | 94.5-96.5 | 96.84 |
| greek_phone | 1045/1047 | 99.81 | 99.3-99.9 | 99.81 |
| greek_patient_name | 774/775 | 99.87 | 99.3-100.0 | 99.93 |
| hospital | 381/521 | 73.13 | 69.2-76.8 | 85.51 |
| amka | 500/500 | 100.00 | 99.2-100.0 | 100.00 |
| dob | 499/500 | 99.80 | 98.9-100.0 | 99.80 |
| greek_clinician | 500/500 | 100.00 | 99.2-100.0 | 100.00 |
| gr_id | 483/483 | 100.00 | 99.2-100.0 | 100.00 |
| url | 141/141 | 100.00 | 97.3-100.0 | 100.00 |
| email | 129/129 | 100.00 | 97.1-100.0 | 100.00 |

## Recall by specialty (identifier-level)
| Specialty | Removed/Total | % | 95% CI |
|---|---|---|---|
| cardiac surgery | 4862/5018 | 96.89 | 96.4-97.3 |
| cardiology | 1406/1462 | 96.17 | 95.1-97.0 |
| nephrology | 1399/1457 | 96.02 | 94.9-96.9 |

## Must-survive probes kept, by category
| Category | Kept/Total | % |
|---|---|---|
| drug | 1741/1849 | 94.16 |
| diagnosis | 992/993 | 99.90 |
| lab_value | 937/953 | 98.32 |
| greek_clinical_header | 833/835 | 99.76 |
| procedure | 732/737 | 99.32 |
| measurement | 634/649 | 97.69 |
| greek_abbrev | 546/554 | 98.56 |
| eponym | 142/177 | 80.23 |

## Residual leaks (270) - Table 4 material
| Note | Category | Gold value | Surviving part(s) | Whole value survived | Flagged |
|---|---|---|---|---|---|
| ca01_cardiogenic_shock_transfer | address | Αγίου Σίλα | Αγίου, Σίλα | yes | no |
| ca01_cocaine_chest_pain | address | Αγίου Σίλα | Αγίου, Σίλα | yes | no |
| ca01_instent_restenosis | address | Εθνική Οδός Καβάλας Δράμας | Εθνική, Οδός | no | no |
| ca01_nstemi_conservative_elderly | address | 7ης Μεραρχίας 12, Καβάλα 65403 | Μεραρχίας | no | no |
| ca01_nstemi_invasive_day_2 | address | Βασιλίσσης Σοφίας 114, 11527, Αθήνα | 11527, | no | no |
| ca01_pci_access_comp | address | Εθνική Οδός Καβάλας Δράμας | Εθνική, Οδός | no | no |
| ca01_stable_angina_staged_pci | address | Εθνική Οδός Καβάλας Δράμας | Εθνική, Οδός | no | no |
| ca01_stemi_late_presenter | address | Άγιος Σίλας, Καβάλα 65201 | Άγιος, Σίλας, | no | no |
| ca01_stemi_primary_pci | hospital | ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ ΑΘΗΝΩΝ «ΙΠΠΟΚΡΑΤΕΙΟ» | ΑΘΗΝΩΝ | no | no |
| ca01_stent_thrombosis | date | στα τέλη Δεκεμβρίου 2023 | τέλη | no | no |
| ca01_takotsubo | address | Εθνική Οδός Καβάλας Δράμας | Εθνική, Οδός | no | no |
| ca02_amyloid_suspicion | hospital | ΠΓΝ ΑΛΕΞΑΝΔΡΟΥΠΟΛΗΣ | ΠΓΝ | no | no |
| ca02_amyloid_suspicion | address | 6ο χλμ Αλεξανδρούπολης - Μάκρης | χλμ | no | no |
| ca02_athlete_hcm | address | 6ο χλμ Αλεξανδρούπολης - Μάκρης | χλμ | no | no |
| ca02_cardiomyopathy_alcohol | hospital | ΠΓΝ ΑΛΕΞΑΝΔΡΟΥΠΟΛΗΣ | ΠΓΝ | no | no |
| ca02_cardiomyopathy_alcohol | address | 6ο χλμ Αλεξανδρούπολης - Μάκρης, 68100 | χλμ | no | no |
| ca02_endocarditis_excluded | address | 6ο χλμ Αλεξανδρούπολης - Μάκρης | χλμ | no | no |
| ca02_hf_readmission_prevention | hospital | ΠΓΝ ΑΛΕΞΑΝΔΡΟΥΠΟΛΗΣ | ΠΓΝ | no | no |
| ca02_hf_readmission_prevention | address | 6ο χλμ Αλεξανδρούπολης - Μάκρης | χλμ | no | no |
| ca02_hfpef_elderly_diuresed | hospital | ΠΓΝ ΑΛΕΞΑΝΔΡΟΥΠΟΛΗΣ | ΠΓΝ | no | no |
| ca02_hfpef_elderly_diuresed | address | 6ο χλμ Αλεξανδρούπολης - Μάκρης | χλμ | no | no |
| ca02_hypertensive_emergency | hospital | ΠΓΝ ΑΛΕΞΑΝΔΡΟΥΠΟΛΗΣ | ΠΓΝ | no | no |
| ca02_hypertensive_emergency | address | 6ο χλμ Αλεξανδρούπολης - Μάκρης | χλμ | no | no |
| ca02_ortho_hypo | address | 6ο χλμ Αλεξανδρούπολης - Μάκρης | χλμ | no | no |
| ca02_pe_massive_resolved | address | 6ο χλμ Αλεξανδρούπολης - Μάκρης | χλμ | no | no |
| ca02_peripartum_cm | address | 6ο χλμ Αλεξανδρούπολης - Μάκρης | χλμ | no | no |
| ca02_peripartum_cm | address | Κοραή 18 | Κοραή | yes | no |
| ca02_severe_as_tavi | address | 6ο χλμ Αλεξανδρούπολης - Μάκρης | χλμ | no | no |
| ca02_sglt2_ckd_watch | hospital | ΠΓΝ ΑΛΕΞΑΝΔΡΟΥΠΟΛΗΣ | ΠΓΝ | no | no |
| ca02_sglt2_ckd_watch | address | 6ο χλμ Αλεξανδρούπολης - Μάκρης | χλμ | no | no |
| ca03_af_ablation_discharge | address | Περιφερειακή Οδός Θεσσαλονίκης, Νέα Ευκα | Οδός | no | no |
| ca03_af_hyperthyroidism | hospital | ΒΕΝΙΖΕΛΕΙΟ ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ ΗΡΑΚΛΕΙΟΥ | ΗΡΑΚΛΕΙΟΥ | no | no |
| ca03_af_rate_control_elderly | hospital | ΒΕΝΙΖΕΛΕΙΟ ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ ΗΡΑΚΛΕΙΟΥ | ΗΡΑΚΛΕΙΟΥ | no | no |
| ca03_digoxin_toxicity | hospital | ΒΕΝΙΖΕΛΕΙΟ ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ ΗΡΑΚΛΕΙΟΥ | ΗΡΑΚΛΕΙΟΥ | no | no |
| ca03_drug_bradycardia | hospital | ΒΕΝΙΖΕΛΕΙΟ ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ ΗΡΑΚΛΕΙΟΥ | ΗΡΑΚΛΕΙΟΥ | no | no |
| ca03_icd_generator_change | hospital | ΒΕΝΙΖΕΛΕΙΟ ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ ΗΡΑΚΛΕΙΟΥ | ΗΡΑΚΛΕΙΟΥ | no | no |
| ca03_lead_revision | hospital | ΒΕΝΙΖΕΛΕΙΟ ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ ΗΡΑΚΛΕΙΟΥ | ΗΡΑΚΛΕΙΟΥ | no | no |
| ca03_long_qt_screening | hospital | ΒΕΝΙΖΕΛΕΙΟ ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ ΗΡΑΚΛΕΙΟΥ | ΝΟΣΟΚΟΜΕΙΟ | no | no |
| ca03_loop_recorder | hospital | ΒΕΝΙΖΕΛΕΙΟ ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ ΗΡΑΚΛΕΙΟΥ | ΗΡΑΚΛΕΙΟΥ | no | no |
| ca03_new_af_anticoagulation | hospital | ΒΕΝΙΖΕΛΕΙΟ ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ ΗΡΑΚΛΕΙΟΥ | ΗΡΑΚΛΕΙΟΥ | no | no |
| ca03_ppm_sick_sinus | hospital | ΒΕΝΙΖΕΛΕΙΟ ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ ΗΡΑΚΛΕΙΟΥ | ΗΡΑΚΛΕΙΟΥ | no | no |
| ca03_ppm_wound_check | address | Περιφερειακή Οδός Θεσσαλονίκης, Νέα Ευκα | Οδός | no | no |
| ca03_svt_ablation_young | hospital | ΒΕΝΙΖΕΛΕΙΟ ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ ΗΡΑΚΛΕΙΟΥ | ΗΡΑΚΛΕΙΟΥ | no | no |
| ca03_syncope_bifascicular_paced | hospital | ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ ΠΑΠΑΓΕΩΡΓΙΟΥ | ΝΟΣΟΚΟΜΕΙΟ | no | no |
| ca03_syncope_bifascicular_paced | date | 20η Ιουνίου 2024 | Ιουνίου | no | no |
| ca03_vt_icd_implanted | hospital | ΒΕΝΙΖΕΛΕΙΟ ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ ΗΡΑΚΛΕΙΟΥ | ΗΡΑΚΛΕΙΟΥ | no | no |
| ca04_carotid_bruit_workup | address | Μιαούλη 12, Στυλίδα 353 00 | Στυλίδα | no | no |
| ca04_costochondritis | hospital | ΥΓΕΙΑ | ΥΓΕΙΑ | yes | no |
| ca04_fh_cascade | hospital | ΥΓΕΙΑ | ΥΓΕΙΑ | yes | no |
| ca04_long_covid_palpitations | date | στα τέλη Δεκεμβρίου 2022 | τέλη | no | no |
| ca04_pad_claudication | hospital | ΥΓΕΙΑ | ΥΓΕΙΑ | yes | no |
| ca04_preop_cardiac_clearance | hospital | ΥΓΕΙΑ | ΥΓΕΙΑ | yes | no |
| ca04_smoking_cessation | hospital | ΥΓΕΙΑ | ΥΓΕΙΑ | yes | no |
| ca04_sports_ecg | address | Παπασιοπούλου τέρμα | τέρμα | no | no |
| ca04_statin_myalgia | hospital | ΥΓΕΙΑ | ΥΓΕΙΑ | yes | no |
| ca04_stress_echo_positive | address | Αγίου Ιωάννου 25, Αγία Παρασκευή 153 42 | Αγία | no | no |
| cs01_cabg_emerg_failed_pci | address | 17124 | 17124 | yes | no |
| cs01_cabg_plexopathy | hospital | ΩΝΑΣΕΙΟ ΚΑΡΔΙΟΧΕΙΡΟΥΡΓΙΚΟ ΚΕΝΤΡΟ | ΚΑΡΔΙΟΧΕΙΡΟΥΡΓΙΚΟ | no | no |
| cs01_off_pump_cabg | address | 176 74 | 176, 74 | yes | no |
| cs01_off_pump_cabg | address | 121 34 | 34 | no | no |
| cs01_off_pump_cabg | date | το Σεπτέμβριο | Σεπτέμβριο | yes | no |
| cs02_avr_dental | date | Μάρτιο του 2024 | Μάρτιο | yes | no |
| cs02_avr_mediastinitis | dob | 14 Μαρτίου 1955 | Μαρτίου | no | no |
| cs02_avr_obese | address | Μαρτίου 22 | Μαρτίου | yes | no |
| cs03_mitral_athlete | hospital | ΝΟΣΟΚΟΜΕΙΟ ΥΓΕΙΑ | ΝΟΣΟΚΟΜΕΙΟ | no | no |
| cs03_mitral_chordal | hospital | ΝΟΣΟΚΟΜΕΙΟ ΥΓΕΙΑ | ΝΟΣΟΚΟΜΕΙΟ | no | no |
| cs03_mitral_postop_af | hospital | METROPOLITAN HOSPITAL | HOSPITAL | no | no |
| cs03_mitral_repair_barlow | hospital | METROPOLITAN HOSPITAL | HOSPITAL | no | no |
| cs03_mitral_repair_barlow | address | Εθν. Μακαρίου 9 | Εθν., Μακαρίου | yes | no |
| cs03_mitral_repair_barlow | address | Νέο Φάληρο 18547 | Νέο | no | no |
| cs03_mitral_repair_failed_mvr | hospital | ΥΓΕΙΑ | ΥΓΕΙΑ | yes | no |
| cs03_mitral_repair_minimally_invasive | hospital | ΕΡΡΙΚΟΣ ΝΤΥΝΑΝ HOSPITAL CENTER | HOSPITAL, CENTER | no | no |
| cs03_mitral_repair_p2 | hospital | ΕΡΡΙΚΟΣ ΝΤΥΝΑΝ HOSPITAL CENTER | HOSPITAL, CENTER | no | no |
| cs03_mitral_repair_ring | hospital | METROPOLITAN HOSPITAL | HOSPITAL | no | no |
| cs03_mitral_repair_ring | address | Εθν. Μακαρίου 9 | Εθν., Μακαρίου | yes | no |
| cs03_mitral_resid_mr | hospital | ΕΡΡΙΚΟΣ ΝΤΥΝΑΝ HOSPITAL CENTER | HOSPITAL, CENTER | no | no |
| cs03_mitral_sam | hospital | ΕΡΡΙΚΟΣ ΝΤΥΝΑΝ HOSPITAL CENTER | HOSPITAL, CENTER | no | no |
| cs03_mvr_anticoag | hospital | METROPOLITAN HOSPITAL | HOSPITAL | no | no |
| cs03_mvr_anticoag | address | Νέο Φάληρο 18547 | Νέο | no | no |
| cs03_mvr_bioprosthetic_elderly | hospital | ΕΡΡΙΚΟΣ ΝΤΥΝΑΝ HOSPITAL CENTER | HOSPITAL, CENTER | no | no |
| cs03_mvr_cabg | hospital | ΕΡΡΙΚΟΣ ΝΤΥΝΑΝ HOSPITAL CENTER | HOSPITAL, CENTER | no | no |
| cs03_mvr_endocarditis_ivdu | address | Εθν. Μακαρίου 9 | Εθν., Μακαρίου | yes | no |
| cs03_mvr_haemolysis | hospital | ΕΡΡΙΚΟΣ ΝΤΥΝΑΝ HOSPITAL CENTER | HOSPITAL, CENTER | no | no |
| cs03_mvr_icu_stay | hospital | ΕΡΡΙΚΟΣ ΝΤΥΝΑΝ HOSPITAL CENTER | HOSPITAL, CENTER | no | no |
| cs03_mvr_mechanical | hospital | ΥΓΕΙΑ | ΥΓΕΙΑ | yes | no |
| cs03_mvr_pulm_htn | hospital | ΝΟΣΟΚΟΜΕΙΟ ΥΓΕΙΑ | ΝΟΣΟΚΟΜΕΙΟ | no | no |
| cs03_mvr_redo | address | Ποσειδώνος 44 | Ποσειδώνος | yes | no |
| cs03_mvr_rehab | hospital | ΝΟΣΟΚΟΜΕΙΟ ΥΓΕΙΑ | ΝΟΣΟΚΟΜΕΙΟ | no | no |
| cs03_mvr_rheumatic_stenosis | hospital | ΥΓΕΙΑ | ΥΓΕΙΑ | yes | no |
| cs03_mvr_stroke_rehab | hospital | ΕΡΡΙΚΟΣ ΝΤΥΝΑΝ HOSPITAL CENTER | HOSPITAL, CENTER | no | no |
| cs04_aneurysm_cabg_combined | hospital | ΠΑΓΝΗ - ΠΑΝΕΠΙΣΤΗΜΙΑΚΟ ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ | ΗΡΑΚΛΕΙΟΥ | no | no |
| cs04_aneurysm_copd_optimisation | hospital | ΠΑΓΝΗ - ΠΑΝΕΠΙΣΤΗΜΙΑΚΟ ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ | ΗΡΑΚΛΕΙΟΥ | no | no |
| cs04_aneurysm_uncontrolled_htn | date | αρχές Απριλίου | αρχές, Απριλίου | yes | no |
| cs04_arch_surgery_neuroprotection | hospital | ΠΑΓΝΗ - ΠΑΝΕΠΙΣΤΗΜΙΑΚΟ ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ | ΗΡΑΚΛΕΙΟΥ | no | no |
| cs04_arch_surgery_neuroprotection | date | αρχές Μαρτίου | αρχές, Μαρτίου | yes | no |
| cs04_asc_aneurysm_elective | address | Ρίο 26504 | Ρίο | no | no |
| cs04_bentall_marfan | hospital | ΠΓΝ Ιωαννίνων | ΠΓΝ | no | no |
| cs04_chronic_dissection_surveillance | hospital | ΠΑΓΝΗ - ΠΑΝΕΠΙΣΤΗΜΙΑΚΟ ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ | ΗΡΑΚΛΕΙΟΥ | no | no |
| cs04_chronic_dissection_surveillance | address | 62 Μαρτύρων 110, 71304 Ηράκλειο | Μαρτύρων | no | no |
| cs04_david_procedure | hospital | ΠΑΝΕΠΙΣΤΗΜΙΑΚΟ ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ ΗΡΑΚΛΕΙ | ΗΡΑΚΛΕΙΟΥ | no | no |
| cs04_dissection_pericardial_effusion | hospital | ΠΑΓΝΗ - ΠΑΝΕΠΙΣΤΗΜΙΑΚΟ ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ | ΗΡΑΚΛΕΙΟΥ | no | no |
| cs04_dissection_tight_bp_control | hospital | ΠΑΓΝΗ - ΠΑΝΕΠΙΣΤΗΜΙΑΚΟ ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ | ΗΡΑΚΛΕΙΟΥ | no | no |
| cs04_elective_arch_staged | date | Μάρτιο του 2022 | Μάρτιο | yes | no |
| cs04_island_transfer | hospital | Γενικό Νοσοκομείο Χανίων | Νοσοκομείο | no | no |
| cs04_paraplegia_scare | address | Ρίο 26504 | Ρίο | no | no |
| cs04_type_a_repair | address | Ρίο 26504 | Ρίο | no | no |
| cs05_asd_flutter_ablation | hospital | ΩΝΑΣΕΙΟ ΚΑΡΔΙΟΧΕΙΡΟΥΡΓΙΚΟ ΚΕΝΤΡΟ | ΚΑΡΔΙΟΧΕΙΡΟΥΡΓΙΚΟ | no | no |
| cs05_mdt_summary | hospital | ΩΝΑΣΕΙΟ ΚΑΡΔΙΟΧΕΙΡΟΥΡΓΙΚΟ ΚΕΝΤΡΟ | ΚΑΡΔΙΟΧΕΙΡΟΥΡΓΙΚΟ | no | no |
| cs05_mdt_summary | date | τέλη Φεβρουαρίου | τέλη, Φεβρουαρίου | yes | no |
| cs06_10_endo_mdt_note | hospital | ΝΙΜΤΣ (417 ΝΟΣΗΛΕΥΤΙΚΟ ΙΔΡΥΜΑ ΜΕΤΟΧΙΚΟΥ  | ΝΟΣΗΛΕΥΤΙΚΟ, ΙΔΡΥΜΑ, ΜΕΤΟΧΙΚΟΥ, ΤΑΜΕΙΟΥ, | no | no |
| cs06_12_pfe_resection | hospital | ΝΙΜΤΣ (417 ΝΟΣΗΛΕΥΤΙΚΟ ΙΔΡΥΜΑ ΜΕΤΟΧΙΚΟΥ  | ΝΟΣΗΛΕΥΤΙΚΟ, ΙΔΡΥΜΑ, ΜΕΤΟΧΙΚΟΥ, ΤΑΜΕΙΟΥ, | no | no |
| cs06_2_pve_reop | hospital | ΝΙΜΤΣ (417 ΝΟΣΗΛΕΥΤΙΚΟ ΙΔΡΥΜΑ ΜΕΤΟΧΙΚΟΥ  | ΝΟΣΗΛΕΥΤΙΚΟ, ΙΔΡΥΜΑ, ΜΕΤΟΧΙΚΟΥ, ΤΑΜΕΙΟΥ, | no | no |
| cs06_4_mitral_hf_urgent | hospital | ΝΙΜΤΣ (417 ΝΟΣΗΛΕΥΤΙΚΟ ΙΔΡΥΜΑ ΜΕΤΟΧΙΚΟΥ  | ΝΟΣΗΛΕΥΤΙΚΟ, ΙΔΡΥΜΑ, ΜΕΤΟΧΙΚΟΥ, ΤΑΜΕΙΟΥ, | no | no |
| cs06_4_mitral_hf_urgent | address | Μονής Πετράκη 10, Αθήνα 115 21 | Μονής | no | no |
| cs06_6_dialysis_endo | hospital | ΝΙΜΤΣ (417 ΝΟΣΗΛΕΥΤΙΚΟ ΙΔΡΥΜΑ ΜΕΤΟΧΙΚΟΥ  | ΝΟΣΗΛΕΥΤΙΚΟ, ΙΔΡΥΜΑ, ΜΕΤΟΧΙΚΟΥ, ΤΑΜΕΙΟΥ, | no | no |
| cs06_6_dialysis_endo | address | Μονής Πετράκη 10, Αθήνα 115 21 | Μονής | no | no |
| cs06_8_tricuspid_ivdu | hospital | ΝΙΜΤΣ (417 ΝΟΣΗΛΕΥΤΙΚΟ ΙΔΡΥΜΑ ΜΕΤΟΧΙΚΟΥ  | ΝΟΣΗΛΕΥΤΙΚΟ, ΙΔΡΥΜΑ, ΜΕΤΟΧΙΚΟΥ, ΤΑΜΕΙΟΥ, | no | no |
| cs06_effusion_malignant_pall | hospital | ΝΟΣΗΛΕΥΤΙΚΟ ΙΔΡΥΜΑ ΜΕΤΟΧΙΚΟΥ ΤΑΜΕΙΟΥ ΣΤΡ | ΤΑΜΕΙΟΥ, ΣΤΡΑΤΟΥ | no | no |
| cs06_lv_aneurysm_repair | hospital | ΝΟΣΗΛΕΥΤΙΚΟ ΙΔΡΥΜΑ ΜΕΤΟΧΙΚΟΥ ΤΑΜΕΙΟΥ ΣΤΡ | ΝΟΣΗΛΕΥΤΙΚΟ, ΙΔΡΥΜΑ, ΜΕΤΟΧΙΚΟΥ, ΤΑΜΕΙΟΥ, | no | no |
| cs06_myectomy_lbbb | hospital | ΝΟΣΗΛΕΥΤΙΚΟ ΙΔΡΥΜΑ ΜΕΤΟΧΙΚΟΥ ΤΑΜΕΙΟΥ ΣΤΡ | ΝΟΣΗΛΕΥΤΙΚΟ, ΙΔΡΥΜΑ, ΜΕΤΟΧΙΚΟΥ, ΤΑΜΕΙΟΥ, | no | no |
| cs06_pericardial_window_effusion | hospital | ΝΟΣΗΛΕΥΤΙΚΟ ΙΔΡΥΜΑ ΜΕΤΟΧΙΚΟΥ ΤΑΜΕΙΟΥ ΣΤΡ | ΝΟΣΗΛΕΥΤΙΚΟ, ΙΔΡΥΜΑ, ΜΕΤΟΧΙΚΟΥ, ΤΑΜΕΙΟΥ, | no | no |
| cs06_pericardiectomy_tb | date | στα μέσα του 1993 | μέσα | yes | no |
| cs06_ventricular_pseudoaneurysm | hospital | ΝΟΣΗΛΕΥΤΙΚΟ ΙΔΡΥΜΑ ΜΕΤΟΧΙΚΟΥ ΤΑΜΕΙΟΥ ΣΤΡ | ΝΟΣΗΛΕΥΤΙΚΟ, ΙΔΡΥΜΑ, ΜΕΤΟΧΙΚΟΥ, ΤΑΜΕΙΟΥ, | no | no |
| cs06_ventricular_pseudoaneurysm | address | Μεγάλου Αλεξάνδρου 12 | Μεγάλου | no | no |
| cs06_ventricular_pseudoaneurysm | date | στα τέλη Απριλίου 2024 | τέλη, Απριλίου | no | no |
| cs07_lvad_inr | date | Ιανουάριο 2023 | Ιανουάριο | no | no |
| cs07_lvad_stroke | date | Μάρτιο του 2021 | Μάρτιο | yes | no |
| cs08_avr_cabg_carotid_stent_first | hospital | ΠΓΝ ΛΑΡΙΣΑΣ | ΠΓΝ | no | no |
| cs08_avr_cabg_carotid_stent_first | address | Περιοχή Μεζούρλο, Λάρισα 41110 | Περιοχή | no | no |
| cs08_avr_cabg_carotid_stent_first | date | στα τέλη Φεβρουαρίου 2024 | τέλη | no | no |
| cs08_avr_cabg_carotid_stent_first | date | στις αρχές Μαρτίου 2024 | αρχές | no | no |
| cs08_avr_mvr_anticoagulation_complexity | hospital | ΠΓΝ ΛΑΡΙΣΑΣ | ΠΓΝ | no | no |
| cs08_cabg_avr_79_year_old | hospital | ΠΓΝ ΛΑΡΙΣΑΣ | ΠΓΝ | no | no |
| cs08_cabg_avr_diabetic_foot_care_aside | hospital | ΠΓΝ ΛΑΡΙΣΑΣ | ΠΓΝ | no | no |
| cs08_cabg_mvr_recurrent_effusions | hospital | ΠΓΝ ΛΑΡΙΣΑΣ | ΠΓΝ | no | no |
| cs08_cabg_mvr_recurrent_effusions | address | ΠΕΡΙΟΧΗ ΜΕΖΟΥΡΛΟ, ΛΑΡΙΣΑ 41110 | ΠΕΡΙΟΧΗ | no | no |
| cs08_combined_amyloid_suspicion_noted | hospital | ΠΓΝ ΛΑΡΙΣΑΣ | ΠΓΝ | no | no |
| cs08_combined_family_meeting_documented | hospital | ΠΓΝ ΙΩΑΝΝΙΝΩΝ | ΠΓΝ | no | no |
| cs08_combined_nutrition_consult | hospital | ΠΓΝ ΙΩΑΝΝΙΝΩΝ | ΠΓΝ | no | no |
| cs08_combined_prolonged_inotropes | hospital | ΠΓΝ ΙΩΑΝΝΙΝΩΝ | ΠΓΝ | no | no |
| cs08_combined_readmitted_day_9_wound | hospital | ΠΓΝ ΙΩΑΝΝΙΝΩΝ | ΠΓΝ | no | no |
| cs08_combined_readmitted_day_9_wound | address | ΛΕΩΦ. ΣΤΑΥΡΟΥ ΝΙΑΡΧΟΥ, ΙΩΑΝΝΙΝΑ 45500 | ΛΕΩΦ. | no | no |
| cs08_combined_rehab_transfer | hospital | ΠΓΝ ΙΩΑΝΝΙΝΩΝ | ΠΓΝ | no | no |
| cs08_tracheostomy_weaned | hospital | ΠΓΝ ΙΩΑΝΝΙΝΩΝ | ΠΓΝ | no | no |
| cs09_avr_concierge | hospital | METROPOLITAN GENERAL | METROPOLITAN, GENERAL | yes | no |
| cs09_avr_concierge | address | Ποσειδώνος 88, Γλυφάδα 166 74 | Ποσειδώνος | no | no |
| cs09_avr_dental_followup | hospital | METROPOLITAN GENERAL | METROPOLITAN, GENERAL | yes | no |
| cs09_avr_early_dc | hospital | METROPOLITAN GENERAL | METROPOLITAN, GENERAL | yes | no |
| cs09_avr_elderly_daughter | hospital | METROPOLITAN GENERAL | METROPOLITAN, GENERAL | yes | no |
| cs09_avr_private_insurer | hospital | METROPOLITAN GENERAL | METROPOLITAN, GENERAL | yes | no |
| cs09_avr_private_insurer | address | Υψηλάντου 33, Παλαιό Φάληρο 175 62 | Παλαιό | no | no |
| cs09_avr_tavi_savr | hospital | METROPOLITAN GENERAL | METROPOLITAN, GENERAL | yes | no |
| cs09_cabg_executive | hospital | METROPOLITAN GENERAL | METROPOLITAN, GENERAL | yes | no |
| cs09_cabg_international | hospital | ΙΑΤΡΙΚΟ ΚΕΝΤΡΟ ΑΘΗΝΩΝ | ΙΑΤΡΙΚΟ | no | no |
| cs09_cabg_international | address | Ermou 15, Athens 105 63 | Ermou | no | no |
| cs09_cabg_premium_room | hospital | ΙΑΤΡΙΚΟ ΚΕΝΤΡΟ ΑΘΗΝΩΝ | ΙΑΤΡΙΚΟ | no | no |
| cs09_cabg_rehab | hospital | ΙΑΤΡΙΚΟ ΚΕΝΤΡΟ ΑΘΗΝΩΝ | ΙΑΤΡΙΚΟ | no | no |
| cs09_cabg_sameweek_angio | hospital | ΙΑΤΡΙΚΟ ΚΕΝΤΡΟ ΑΘΗΝΩΝ | ΙΑΤΡΙΚΟ | no | no |
| cs09_cabg_sleep_apnoea | hospital | ΙΑΤΡΙΚΟ ΚΕΝΤΡΟ ΑΘΗΝΩΝ | ΙΑΤΡΙΚΟ | no | no |
| cs09_cabg_wound_clinic | hospital | ΙΑΤΡΙΚΟ ΚΕΝΤΡΟ ΑΘΗΝΩΝ | ΙΑΤΡΙΚΟ | no | no |
| cs09_cabg_wound_clinic | date | 12 Νοεμβρίου 2023 | Νοεμβρίου | no | no |
| cs09_cabg_wound_clinic | date | 13 Νοεμβρίου | Νοεμβρίου | yes | no |
| cs09_cabg_wound_clinic | date | 19 Νοεμβρίου 2023 | Νοεμβρίου | no | no |
| cs09_cabg_wound_clinic | date | 23 Νοεμβρίου 2023 | Νοεμβρίου | no | no |
| cs09_mitral_cd | hospital | METROPOLITAN GENERAL | METROPOLITAN, GENERAL | yes | no |
| cs09_mitral_flight_islander | hospital | METROPOLITAN GENERAL | METROPOLITAN, GENERAL | yes | no |
| cs09_mitral_robotic | hospital | METROPOLITAN GENERAL | METROPOLITAN, GENERAL | yes | no |
| cs09_mitral_second_opinion | hospital | METROPOLITAN GENERAL | METROPOLITAN, GENERAL | yes | no |
| cs09_mitral_yoga | hospital | METROPOLITAN GENERAL | METROPOLITAN, GENERAL | yes | no |
| cs09_valve_choice | hospital | METROPOLITAN GENERAL | METROPOLITAN, GENERAL | yes | no |
| cs10_bleeding | address | Ρίο Πατρών, 265 04 | Ρίο | no | no |
| cs10_complete_heart_block | address | Κάτω Αχαΐα 25200 | Κάτω | no | no |
| cs10_dehiscence | address | Ρίο Πατρών, 265 04 | Ρίο | no | no |
| cs10_hyperglycaemia | hospital | ΩΝΑΣΕΙΟ ΚΑΡΔΙΟΧΕΙΡΟΥΡΓΙΚΟ ΚΕΝΤΡΟ | ΚΑΡΔΙΟΧΕΙΡΟΥΡΓΙΚΟ | no | no |
| cs10_pericarditis | address | Ρίο | Ρίο | yes | no |
| cs10_phrenic | date | 12 ημέρες | ημέρες | yes | no |
| cs10_pneumonia | address | Ρίο Πατρών, 265 04 | Ρίο | no | no |
| cs10_readmission_avoided | address | Ρίο | Ρίο | yes | no |
| cs10_stroke | hospital | ΩΝΑΣΕΙΟ ΚΑΡΔΙΟΧΕΙΡΟΥΡΓΙΚΟ ΚΕΝΤΡΟ | ΚΑΡΔΙΟΧΕΙΡΟΥΡΓΙΚΟ | no | no |
| cs10_tia | address | Ρίο Πατρών, 265 04 | Ρίο | no | no |
| cs10_tracheostomy | date | 40 ημέρες | ημέρες | yes | no |
| cs10_vac | date | 15/01 | 15/01 | yes | no |
| cs10_vac | date | 18/01 | 18/01 | yes | no |
| cs10_vac | date | 21/01 | 21/01 | yes | no |
| cs10_vac | date | 25/01 | 25/01 | yes | no |
| cs11_mitraclip | hospital | ΕΡΡΙΚΟΣ ΝΤΥΝΑΝ HOSPITAL CENTER | HOSPITAL, CENTER | no | no |
| cs11_mitral_highrisk_redo | date | 08/09 | 08/09 | yes | no |
| cs11_pfo_closure | hospital | ΕΡΡΙΚΟΣ ΝΤΥΝΑΝ HOSPITAL CENTER | HOSPITAL, CENTER | no | no |
| cs11_tavi_dialysis | hospital | ΕΡΡΙΚΟΣ ΝΤΥΝΑΝ HOSPITAL CENTER | HOSPITAL, CENTER | no | no |
| cs11_tavi_echo_qc | hospital | ΕΡΡΙΚΟΣ ΝΤΥΝΑΝ HOSPITAL CENTER | HOSPITAL, CENTER | no | no |
| cs11_tavi_femoral_haematoma | date | 12/01 | 12/01 | yes | no |
| cs11_tavi_femoral_haematoma | date | 14/01-16/01 | 14/01-16/01 | yes | no |
| cs11_tavi_frailty | hospital | ΕΡΡΙΚΟΣ ΝΤΥΝΑΝ HOSPITAL CENTER | HOSPITAL, CENTER | no | no |
| cs11_tavi_nonagenarian | hospital | ΕΡΡΙΚΟΣ ΝΤΥΝΑΝ HOSPITAL CENTER | HOSPITAL, CENTER | no | no |
| cs11_tavi_ppm | hospital | ΕΡΡΙΚΟΣ ΝΤΥΝΑΝ HOSPITAL CENTER | HOSPITAL, CENTER | no | no |
| cs11_tavi_readmit_hf | hospital | ΕΡΡΙΚΟΣ ΝΤΥΝΑΝ HOSPITAL CENTER | HOSPITAL, CENTER | no | no |
| cs11_tavi_readmit_hf | date | 11/02 | 11/02 | yes | no |
| cs11_tavi_readmit_hf | date | 15/02 | 15/02 | yes | no |
| cs11_tavi_rehab_rural | hospital | ΕΡΡΙΚΟΣ ΝΤΥΝΑΝ HOSPITAL CENTER | HOSPITAL, CENTER | no | no |
| cs11_tavi_stroke_protect | hospital | ΕΡΡΙΚΟΣ ΝΤΥΝΑΝ HOSPITAL CENTER | HOSPITAL, CENTER | no | no |
| cs11_tavi_vascular_complication | hospital | ΕΡΡΙΚΟΣ ΝΤΥΝΑΝ HOSPITAL CENTER | HOSPITAL, CENTER | no | no |
| cs11_tricuspid_teer | date | Αύγουστο 2023 | Αύγουστο | no | no |
| cs12_avr_farmer | hospital | ΠΑΝΕΠΙΣΤΗΜΙΑΚΟ ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ ΗΡΑΚΛΕΙ | ΗΡΑΚΛΕΙΟΥ | no | no |
| cs12_cabg_woman | address | Αιγαίου 12, Νέα Σμύρνη 17121 | Νέα | no | no |
| cs12_combined_valve_rheumatic | date | Ιουλίου | Ιουλίου | yes | no |
| cs12_dissection_imaging | date | Φεβρουάριο του 2023 | Φεβρουάριο | yes | no |
| cs12_lvad_carer | hospital | ΠΑΓΝΗ - ΠΑΝΕΠΙΣΤΗΜΙΑΚΟ ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ | ΗΡΑΚΛΕΙΟΥ | no | no |
| cs12_mitral_musician | hospital | ΓΝΑ «Ο ΕΥΑΓΓΕΛΙΣΜΟΣ» | ΓΝΑ | no | no |
| cs12_myectomy_athlete | hospital | ΓΝΑ «Ο ΕΥΑΓΓΕΛΙΣΜΟΣ» | ΓΝΑ | no | no |
| cs12_pericardiectomy_tb | address | Αγίου Τίτου 10, Μοίρες 70400 | Μοίρες | no | no |
| cs12_tavi_granddaughter | hospital | ΓΝΑ «Ο ΕΥΑΓΓΕΛΙΣΜΟΣ» | ΓΝΑ | no | no |
| cs12_vsr_survivor | date | Ιανουαρίου 2024 | Ιανουαρίου | no | no |
| ne01_hyponatraemia_siadh | date | από τα τέλη Σεπτεμβρίου 2023 | τέλη | no | no |
| ne02_apd_cycler | address | 2ο χλμ Ε.Ο. Σερρών-Δράμας | χλμ | no | no |
| ne02_cath_exchange | address | 2ο χλμ Ε.Ο. Σερρών-Δράμας | χλμ | no | no |
| ne02_cath_infection | hospital | ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ ΘΕΣΣΑΛΟΝΙΚΗΣ "ΙΠΠΟΚΡΑΤ | ΘΕΣΣΑΛΟΝΙΚΗΣ | no | no |
| ne02_conservative_care | hospital | ΙΔΙΩΤΙΚΗ ΚΛΙΝΙΚΗ "ΑΓΙΟΣ ΛΟΥΚΑΣ" ΣΕΡΡΩΝ | ΙΔΙΩΤΙΚΗ, ΚΛΙΝΙΚΗ | no | no |
| ne02_dry_weight | address | 2ο χλμ Ε.Ο. Σερρών-Δράμας | χλμ | no | no |
| ne02_esa_titration | address | 2ο χλμ Εθνικής Οδού Σερρών - Δράμας | χλμ, Εθνικής, Οδού, Δράμας | no | no |
| ne02_fistula_declot | hospital | ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ ΘΕΣΣΑΛΟΝΙΚΗΣ "ΙΠΠΟΚΡΑΤ | ΘΕΣΣΑΛΟΝΙΚΗΣ | no | no |
| ne02_fistula_steal | address | 2ο χλμ Ε.Ο. Σερρών-Δράμας | χλμ | no | no |
| ne02_hd_adequacy | hospital | ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ ΘΕΣΣΑΛΟΝΙΚΗΣ "ΙΠΠΟΚΡΑΤ | ΘΕΣΣΑΛΟΝΙΚΗΣ | no | no |
| ne02_hd_diet_k | hospital | ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ ΘΕΣΣΑΛΟΝΙΚΗΣ "ΙΠΠΟΚΡΑΤ | ΘΕΣΣΑΛΟΝΙΚΗΣ | no | no |
| ne02_hd_hf_ultra | hospital | ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ ΘΕΣΣΑΛΟΝΙΚΗΣ "ΙΠΠΟΚΡΑΤ | ΘΕΣΣΑΛΟΝΙΚΗΣ | no | no |
| ne02_hd_hf_ultra | date | 13/04 | 13/04 | yes | no |
| ne02_hd_hf_ultra | date | 20/04 | 20/04 | yes | no |
| ne02_intradialytic_htn | address | 2ο χλμ Ε.Ο. Σερρών-Δράμας | χλμ | no | no |
| ne02_pd_peritonitis | address | 2ο χλμ Ε.Ο. Σερρών-Δράμας | χλμ | no | no |
| ne02_pd_to_hd | hospital | ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ ΘΕΣΣΑΛΟΝΙΚΗΣ "ΙΠΠΟΚΡΑΤ | ΘΕΣΣΑΛΟΝΙΚΗΣ | no | no |
| ne02_pd_to_hd | date | 18ης | 18ης | yes | no |
| ne02_pd_to_hd | date | 21ης Ιουνίου | Ιουνίου | yes | no |
| ne02_pd_training | hospital | ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ ΘΕΣΣΑΛΟΝΙΚΗΣ "ΙΠΠΟΚΡΑΤ | ΘΕΣΣΑΛΟΝΙΚΗΣ | no | no |
| ne02_phosphate_switch | address | 2ο χλμ Εθνικής Οδού Σερρών - Δράμας | χλμ, Εθνικής, Οδού, Δράμας | no | no |
| ne02_phosphate_switch | address | Εθνικής Αντιστάσεως 55 | Εθνικής | no | no |
| ne02_travel_plan | address | 2ο χλμ Εθνικής Οδού Σερρών - Δράμας | χλμ, Εθνικής, Οδού, Δράμας | no | no |
| ne02_uraemic_pericarditis | address | 2ο χλμ Εθνικής Οδού Σερρών - Δράμας | χλμ, Εθνικής, Οδού, Δράμας | no | no |
| ne02_uraemic_pericarditis | date | 10/05 | 10/05 | yes | no |
| ne02_uraemic_pericarditis | date | 12/05 | 12/05 | yes | no |
| ne02_vein_mapping | address | 2ο χλμ Εθνικής Οδού Σερρών - Δράμας | χλμ, Εθνικής, Οδού, Δράμας | no | no |
| ne03_donor_annual_followup | hospital | ΙΔΙΩΤΙΚΟ ΝΕΦΡΟΛΟΓΙΚΟ ΙΑΤΡΕΙΟ (ΣΥΝΕΡΓΑΤΗΣ | ΙΔΙΩΤΙΚΟ, ΝΕΦΡΟΛΟΓΙΚΟ, ΙΑΤΡΕΙΟ, (ΣΥΝΕΡΓΑ | no | no |
| ne03_donor_annual_followup | date | Οκτώβριο του 2018 | Οκτώβριο | yes | no |
| ne03_donor_annual_followup | hospital | ΠΓΝ Ιωαννίνων | ΠΓΝ | no | no |
| ne03_donor_annual_followup | date | Νοέμβριο του 2024 | Νοέμβριο | yes | no |
| ne03_graft_failure_dialysis | hospital | ΠΓΝ ΙΩΑΝΝΙΝΩΝ | ΠΓΝ | no | no |
| ne03_graft_failure_dialysis | date | Μάιο του 2012 | Μάιο | yes | no |
| ne03_graft_failure_dialysis | date | Ιανουάριο 2023 | Ιανουάριο | no | no |
| ne03_nodat_education | hospital | ΠΓΝ ΙΩΑΝΝΙΝΩΝ | ΠΓΝ | no | no |
| ne03_nodat_education | date | 01/2024 | 01/2024 | yes | no |
| ne03_nonadherence_addressed | hospital | ΠΓΝ ΙΩΑΝΝΙΝΩΝ | ΠΓΝ | no | no |
| ne03_transplant_bp | hospital | ΠΓΝ ΙΩΑΝΝΙΝΩΝ | ΠΓΝ | no | no |
| ne03_transplant_bp | date | Φεβρουάριο του 2021 | Φεβρουάριο | yes | no |
| ne03_transplant_travel_advice | hospital | ΙΔΙΩΤΙΚΟ ΙΑΤΡΕΙΟ ΝΕΦΡΟΛΟΓΙΑΣ ΚΑΙ ΜΕΤΑΜΟΣ | ΙΔΙΩΤΙΚΟ, ΙΑΤΡΕΙΟ, ΝΕΦΡΟΛΟΓΙΑΣ, ΜΕΤΑΜΟΣΧ | no | no |
| ne03_transplant_travel_advice | date | Σεπτέμβριο του 2023 | Σεπτέμβριο | yes | no |
| ne03_transplant_vaccination | date | Οκτώβριο 2022 | Οκτώβριο | no | no |
| ne03_tx_pyelonephritis | greek_phone | 2651099887 | 2651099887 | yes | YES |
| ne04_01_dialysis_tourist | address | Ξενοδοχείο Ήλιος, Φαληράκι, 85105 | Ξενοδοχείο, Ήλιος, | no | no |
| ne04_02_remote_ckd_telemed | hospital | ΠΑΝΕΠΙΣΤΗΜΙΑΚΟ ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ ΗΡΑΚΛΕΙ | ΗΡΑΚΛΕΙΟΥ | no | no |
| ne04_04_fisherman_leptospirosis | hospital | ΠΑΝΕΠΙΣΤΗΜΙΑΚΟ ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ ΗΡΑΚΛΕΙ | ΗΡΑΚΛΕΙΟΥ | no | no |
| ne04_05_farmer_pesticides | hospital | ΠΑΝΕΠΙΣΤΗΜΙΑΚΟ ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ ΗΡΑΚΛΕΙ | ΗΡΑΚΛΕΙΟΥ | no | no |
| ne04_07_uric_acid_gout | hospital | ΠΑΝΕΠΙΣΤΗΜΙΑΚΟ ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ ΗΡΑΚΛΕΙ | ΗΡΑΚΛΕΙΟΥ | no | no |
| ne04_09_myeloma_cast_nephropathy | hospital | ΠΑΝΕΠΙΣΤΗΜΙΑΚΟ ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ ΗΡΑΚΛΕΙ | ΗΡΑΚΛΕΙΟΥ | no | no |
| ne04_10_amyloidosis_biopsy | address | Ερυθρού Σταυρού, Ρόδος 85100 | Ερυθρού | no | no |
| ne04_11_fabry_screening | hospital | ΠΑΝΕΠΙΣΤΗΜΙΑΚΟ ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ ΗΡΑΚΛΕΙ | ΗΡΑΚΛΕΙΟΥ | no | no |
| ne04_13_thin_basement_membrane | hospital | ΠΑΝΕΠΙΣΤΗΜΙΑΚΟ ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ ΗΡΑΚΛΕΙ | ΗΡΑΚΛΕΙΟΥ | no | no |
| ne04_hepatorenal_bridge | greek_patient_name | Ελένη Μιχαηλίδου | Μιχαηλίδου | no | no |
| ne04_hepatorenal_bridge | date | 11/02 | 11/02 | yes | no |
| ne04_hepatorenal_bridge | date | 12/02 | 12/02 | yes | no |
| ne04_hepatorenal_bridge | date | 14/02 | 14/02 | yes | no |
| ne04_hepatorenal_bridge | date | 15/02 | 15/02 | yes | no |
| ne04_retroperitoneal_fibrosis | greek_phone | 2810223344 | 2810223344 | yes | YES |

## Over-redacted clinical probes (190)
| Note | Category | Value |
|---|---|---|
| ca01_myocarditis_cmr | eponym | Lake Louise |
| ca01_stemi_diabetic_insulin | drug | ινσουλίνης Glargine |
| ca01_stemi_diabetic_insulin | drug | Insulin Glargine (Lantus): 20 διεθνείς μονάδες |
| ca01_stemi_diabetic_insulin | drug | Insulin Lispro (Humalog): 6 διεθνείς μονάδες |
| ca02_athlete_hcm | measurement | VO2 max |
| ca02_pe_intermediate | drug | Apixaban (Eliquis) 10 mg |
| ca02_pe_massive_resolved | eponym | σημείο McConnell |
| ca02_severe_as_tavi | measurement | Vmax): 4.5 m/s |
| ca03_af_rapid_hf | lab_value | Hct 40% |
| ca03_atrial_flutter_ablation | measurement | Hct 44% |
| ca03_electrical_storm_settled | drug | Sacubitril/Valsartan (Entresto) 24/26mg |
| ca03_long_qt_screening | drug | Nadolol (Corgard) 40 mg |
| ca03_long_qt_screening | lab_value | www.crediblemeds.org |
| ca03_svt_ablation_young | eponym | Koch |
| ca04_cpet_dyspnoea | measurement | VO2 max): 22 ml/kg/min |
| ca04_diabetic_silent_ischaemia | eponym | πρωτόκολλο Bruce |
| ca04_fh_cascade | eponym | Dutch Lipid Clinic Network |
| ca04_long_covid_palpitations | diagnosis | λοίμωξη COVID-19 |
| ca04_noac_ckd | drug | Rivaroxaban (Xarelto) 15 mg |
| ca04_obesity_cardiac | eponym | Bruce |
| ca04_valve_click_inr | drug | Acenocoumarol (Sintrom 4mg): Λήψη 1/2 δισκίου καθημερινά |
| cs01_cabg_diabetic_ckd | greek_abbrev | AKI |
| cs01_cabg_plexopathy | greek_abbrev | LIMA |
| cs01_cabg_plexopathy | drug | T. Salospir 100 mg 1x1 |
| cs01_elective_cabg | eponym | LIMA |
| cs01_redo_cabg | eponym | LIMA |
| cs02_avr_asc_aorta | lab_value | Hct 34,2% |
| cs02_avr_bicuspid | drug | Bisoprolol 2.5mg |
| cs02_avr_bio_elderly | drug | Salospir 100mg |
| cs02_avr_cabg | drug | Salospir 100mg |
| cs02_avr_cabg | drug | Clopidogrel 75mg |
| cs02_avr_chb_ppm | drug | Salospir 100mg |
| cs02_avr_chb_ppm | drug | Bisoprolol 2.5mg |
| cs02_avr_mech | drug | Bisoprolol 2.5mg |
| cs02_avr_mediastinitis | drug | Rifampicin |
| cs02_avr_new_af | lab_value | Hct 36% |
| cs02_avr_new_af | drug | Apixaban (Eliquis) 5mg |
| cs02_avr_pleural | lab_value | Hct 35% |
| cs02_avr_pleural | drug | Bisoprolol 2.5mg |
| cs02_avr_pm_dependent | lab_value | Hct 34,5% |
| cs02_avr_pm_dependent | drug | Salospir 100mg |
| cs02_avr_pm_dependent | drug | Bisoprolol 2.5mg |
| cs02_avr_ppm_mismatch | drug | Salospir 100mg |
| cs02_avr_ppm_mismatch | drug | Bisoprolol 2.5mg |
| cs02_avr_pvl | drug | Bisoprolol 5mg |
| cs02_avr_redo | drug | Bisoprolol 5mg |
| cs02_avr_renal | drug | Salospir 100mg |
| cs02_avr_renal | drug | Bisoprolol 5mg |
| cs02_avr_rheumatic | drug | Acenocoumarol (Sintrom) 4mg |
| cs02_avr_sutureless | drug | Salospir 100mg |
| cs02_avr_tamponade | lab_value | Hct 34% |
| cs02_avr_ventilation | drug | Salospir 100mg |
| cs02_avr_ventilation | drug | Bisoprolol 2.5mg |
| cs03_mitral_chordal | procedure | εμφύτευση τεχνητών χορδών από PTFE (Gore-Tex) |
| cs03_mitral_repair_failed_mvr | drug | Sintrom |
| cs03_mitral_repair_maze | drug | Sintrom |
| cs03_mvr_endocarditis_ivdu | drug | Cloxacillin |
| cs03_mvr_mechanical | drug | Sintrom |
| cs03_mvr_rheumatic_stenosis | greek_clinical_header | ΠΕΡΙΛΗΨΗ ΝΟΣΗΛΕΙΑΣ — ΕΞΙΤΗΡΙΟ |
| cs03_mvr_rheumatic_stenosis | eponym | Wilkins |
| cs04_aneurysm_redo_sternotomy | drug | T. Salospir 100 mg |
| cs04_aneurysm_redo_sternotomy | drug | T. Bisoprolol 5 mg |
| cs04_david_procedure | eponym | David |
| cs04_dissection_renal_recovery | drug | Bisoprolol 5 mg |
| cs04_dissection_renal_recovery | drug | Salospir 100 mg |
| cs04_dissection_tight_bp_control | drug | T. Atorvastatin 40 mg |
| cs04_dissection_young_weightlifter | eponym | επέμβαση David |
| cs04_root_abscess | drug | Vancomycin |
| cs04_root_abscess | drug | Rifampicin |
| cs05_asd_min_inv | drug | Aspirin (Salospir) 100 mg |
| cs05_asd_pht_assess | measurement | CO (Fick): 4.5 L/min |
| cs05_asd_transient_af | drug | T. Bisoprolol 2.5 mg 1x1 |
| cs05_congenital_preg_couns | eponym | Bruce |
| cs05_mdt_summary | eponym | Taussig-Bing |
| cs05_mdt_summary | measurement | ροή ~3.5 m/s |
| cs05_pfo_surgical_closure | drug | T. Salospir 100 mg 1x1 |
| cs05_pfo_surgical_closure | drug | T. Bisoprolol 5 mg 1x1 |
| cs05_redo_adhesions | measurement | RVEF 38% |
| cs05_redo_adhesions | drug | Ασπιρίνη (Salospir) 100 mg |
| cs05_vsd_ar_repair | drug | Aspirin (Salospir) 100 mg |
| cs06_10_endo_mdt_note | drug | Salospir 100 mg |
| cs06_11_myxoma_la | drug | Salospir 100 mg |
| cs06_12_pfe_resection | drug | Salospir 100 mg |
| cs06_13_cardiac_tumour_embolic | eponym | Fogarty |
| cs06_13_cardiac_tumour_embolic | drug | Salospir 100 mg |
| cs06_1_native_avr | drug | Salospir 100 mg |
| cs06_1_native_avr | drug | Bisoprolol 5 mg |
| cs06_2_pve_reop | drug | Sintrom |
| cs06_3_septic_emboli | drug | Sintrom |
| cs06_3_septic_emboli | drug | Bisoprolol 2.5 mg |
| cs06_7_root_abscess_homograft | drug | Bisoprolol 5 mg |
| cs06_8_tricuspid_ivdu | drug | Salospir 100 mg |
| cs06_hocm_myectomy | greek_abbrev | SAM |
| cs06_hocm_myectomy | eponym | Morrow |
| cs06_hocm_myectomy | lab_value | Hct 35% |
| cs06_myxoma_followup | eponym | Carney |
| cs06_pericardiectomy_constrictive | drug | Paracetamol 1g |
| cs06_post_infarct_vsr | drug | Bisoprolol 2,5 mg |
| cs06_post_infarct_vsr | drug | Empagliflozin 10 mg |
| cs07_crtd_upgrade | drug | Tab. Sacubitril/Valsartan (Entresto) 49/51 mg |
| cs07_ecmo_wean_cardio | measurement | ροής του ECMO (weaning trial) στο 1.5 L/min |
| cs07_lvad_inr | lab_value | Hct 37% |
| cs07_lvad_inr | drug | Warfarin (Sintrom) |
| cs07_post_tx_dm | drug | Lispro 4-6 μονάδες |
| cs07_post_tx_dm | lab_value | K+ 4.1 mmol/L |
| cs07_post_tx_dm | drug | Insulin Lispro: 4 UI |
| cs07_tx_biopsy | lab_value | Hct 38% |
| cs07_tx_cmv | drug | Mycophenolate Mofetil |
| cs07_tx_listed | measurement | VE/VCO2 slope 42 |
| cs07_tx_postop_dc | drug | Basiliximab |
| cs07_tx_psych | measurement | PHQ-9 απέδωσε σκορ 2 |
| cs07_tx_renal | lab_value | Επίπεδα Tacrolimus (C0) 14.5 ng/mL |
| cs07_tx_workup | eponym | NYHA III-IV |
| cs08_avr_cabg_carotid_stent_first | eponym | Edwards Magna |
| cs08_cabg_myectomy | eponym | Morrow |
| cs08_combined_aki | drug | Sintrom |
| cs08_combined_aki | drug | Zaroxolyn 2.5mg |
| cs08_combined_aki | greek_abbrev | AKI |
| cs08_combined_low_ef | lab_value | BNP: 850 pg/mL |
| cs08_combined_nutrition_consult | eponym | Levin |
| cs08_tracheostomy_weaned | drug | Meropenem 1g |
| cs08_triple_valve | eponym | De Vega |
| cs09_avr_concierge | eponym | Nicks |
| cs09_mitral_flight_islander | lab_value | Hct: 33,5% |
| cs10_aki | greek_abbrev | AKI |
| cs10_complete_heart_block | greek_abbrev | LIMA |
| cs10_delirium_resolved | eponym | Foley |
| cs10_gibleed | eponym | Forrest Ib |
| cs10_hypothyroid | eponym | Hashimoto |
| cs10_pleural_effusion | eponym | del Nido |
| cs10_pneumonia | drug | Meropenem 1g |
| cs10_vac | drug | Rifampicin |
| cs11_laa_occlusion | procedure | Watchman FLX |
| cs11_tavi_femoral_haematoma | greek_clinical_header | ΕΡΓΑΣΤΗΡΙΑΚΟΣ ΕΛΕΓΧΟΣ (Προ εξόδου 17/01/2024): |
| cs11_tavi_frailty | greek_abbrev | NYHA |
| cs11_tavi_frailty | eponym | κλίμακα Katz |
| cs12_cabg_woman | lab_value | Hct 34,5% |
| cs12_endocarditis_student | lab_value | Hct 38% |
| cs12_mitral_postpartum | drug | Tab. Sacubitril/Valsartan (Entresto) 24/26mg: 1x2 |
| cs12_tavi_granddaughter | drug | Apixaban |
| ne01_aki_contrast | drug | Iohexol |
| ne01_ckd4_progression | drug | Karvezide |
| ne01_ckd4_progression | drug | Dapagliflozin |
| ne01_membranous_pla2r | drug | Rituximab 1g |
| ne01_nephrotic_new | greek_abbrev | ANA |
| ne01_obstructive_bph | procedure | ουροκαθετήρα Foley 18Fr |
| ne02_apd_cycler | drug | Extraneal (Icodextrin) |
| ne02_conservative_care | drug | Sodium Bicarbonate (Sodibic) 500 mg |
| ne02_fistula_declot | procedure | θρομβεκτομή με καθετήρα Fogarty |
| ne02_fistula_declot | eponym | Fogarty |
| ne02_hd_adequacy | drug | Sevelamer (Renagel) 800 mg |
| ne02_hd_hf_ultra | eponym | NYHA III |
| ne02_iron_sucrose | drug | Venofer |
| ne02_pd_to_hd | drug | Icodextrin (Extraneal) |
| ne02_pd_training | eponym | Tenckhoff |
| ne02_phosphate_switch | drug | Sevelamer Carbonate |
| ne02_phosphate_switch | drug | Sevelamer Carbonate (Renvela) 800 mg |
| ne02_shpt_cinacalcet | drug | Mimpara |
| ne02_shpt_cinacalcet | drug | Cinacalcet (Mimpara) 30 mg |
| ne02_travel_plan | drug | Tinzaparin (Innohep) 3.500 anti-Xa IU |
| ne03_acr_treated | eponym | Banff 1A |
| ne03_acr_treated | measurement | δείκτη RI (0.65) |
| ne03_bk_viraemia | drug | Mycophenolate Mofetil |
| ne03_bk_viraemia | drug | Tacrolimus |
| ne03_graft_failure_dialysis | drug | Sevelamer (Renagel) 800 mg |
| ne03_graft_gout_interaction | drug | Allopurinol (Zyloric) 300 mg/ημέρα |
| ne03_graft_gout_interaction | drug | Zyloric |
| ne03_graft_gout_interaction | drug | Adenuric (Febuxostat) |
| ne03_graft_stenosis_angioplasty | drug | Aspirin (Salospir) 100 mg |
| ne03_nodat_education | drug | Insulin Degludec - Tresiba) σε χαμηλή δόση (10 μονάδες/ημέρα |
| ne03_nodat_education | drug | Tresiba (Insulin Degludec) 10 μονάδες |
| ne03_nonadherence_addressed | drug | παρατεταμένης αποδέσμευσης (Advagraf) |
| ne03_transplant_bone_disease | measurement | T-score -2.8 στην ΟΜΣΣ και -2.4 στο ισχίο |
| ne03_transplant_bone_disease | procedure | Απλή ακτινογραφία ΟΜΣΣ |
| ne03_transplant_bone_disease | drug | Alphacalcidiol |
| ne03_transplant_bone_disease | drug | Alendronate (Fosamax) 70 mg |
| ne03_transplant_bone_disease | drug | Alphacalcidiol (One-Alpha) 0.25 mcg |
| ne03_transplant_bp | drug | Doxazosin (Maguran) 4 mg |
| ne03_transplant_vaccination | drug | Apexxnar |
| ne03_transplant_vaccination | drug | Pneumovax 23 |
| ne03_tx_pregnancy | measurement | Λεύκωμα < 50 mg/24h |
| ne04_04_fisherman_leptospirosis | eponym | σύνδρομο Weil |
| ne04_06_stone_clinic | measurement | Ασβέστιο ούρων: 310 mg/24h |
| ne04_06_stone_clinic | measurement | Κιτρικά ούρων: 220 mg/24h |
| ne04_09_myeloma_cast_nephropathy | eponym | Bence Jones |
| ne04_12_alport_referral | eponym | Συνδρόμου Alport |
| ne04_cardiorenal_advanced | drug | μετολαζόνης (Zaroxolyn) 2,5 mg |
| ne04_hepatorenal_bridge | drug | τερλιπρεσσίνη (terlipressin) 1 mg |
| ne04_renal_artery_fmd | drug | Ακετυλοσαλικυλικό οξύ (Salospir) 100 mg |
| ne04_retroperitoneal_fibrosis | eponym | νόσος Ormond |