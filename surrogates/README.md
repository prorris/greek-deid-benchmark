# Surrogate pools of the evaluated engine (Morpheus 1.0)

`morpheus_1.0_surrogate_pools.json` lists the pools of artificial replacement
values ("hiding in plain sight" surrogates) that the evaluated engine —
Morpheus 1.0, pipeline fingerprint `765328fbf1241ea4` — drew from when it
produced the outputs in `results/`.

- **Pooled values:** given names, surnames and towns (a Greek-script set, used
  when the original is written in Greek, and a Latin-script set), street
  names and types, e-mail domains, postcode areas, and the templates from
  which a replacement hospital name is composed.
- **Generated values, not pooled:** telephone numbers, postcodes, e-mail local
  parts, identifiers and hospital record numbers are generated to mirror the
  shape of the original; dates are shifted by one random offset per document.
  None of these appear in the file.
- Within one document the same original value always receives the same
  replacement. Replacement values are re-drawn on every run, which is why the
  two result files differ in their surrogates and agree in their decisions.

Only the values are published. The replacement logic is part of the
proprietary engine and is not included.

**Every value here is artificial and was chosen as an ordinary, widely shared
name or place. A replacement name in the outputs refers to no one; any
resemblance to a real person is coincidental.**

The pools of version 1.0 are small. They are published as they were at
evaluation time, so that the outputs in `results/` can be read knowing exactly
which values are replacements.

Licence: CC BY 4.0, as for the rest of the data in this repository.
