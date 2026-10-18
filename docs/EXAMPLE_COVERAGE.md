# Sample coverage index — all samples are `.ostf` (UTF-8 JSON)

All samples use the same schema. They are valid reference **examples**, not a claim that every possible musical scenario is covered. Normative chord and scale ID vocabularies are exhaustively represented.

| Coverage | Sample |
|---|---|
| International Unicode song and section names, key changes, full code timeline | `01_international_song.ostf` |
| Meter changes, additive beat groups, interrupted/incomplete bars | `02_meter_partial_bars.ostf` |
| Pickup duration, compound meter, explicit N.C. | `03_pickup_no_chord.ostf` |
| Linear quarter-BPM ramps, step tempo, dotted-quarter beat unit | `04_tempo_ramp_dotted_beat.ostf` |
| Enharmonic pitch spelling, slash bass, degree add/alter/omit, simultaneous b9/#9, unknown harmony gap, vendor extensions | `05_harmony_operations_and_gaps.ostf` |
| All 25 registered chord quality IDs | `06_all_25_chord_qualities.ostf` |
| All 20 registered scale IDs | `07_all_20_scales.ostf` |
| Gaps between sections, no-chord distinct from unspecified harmony | `08_sections_gaps_unspecified_harmony.ostf` |
| Rational triplet onset and non-PPQ precision | `09_rational_triplets.ostf` |
| Original audited stable fixtures converted to `.ostf` | `mixed_meter_song.ostf`, `pickup_tempo_ramp.ostf`, `harmony_extensions.ostf`, `dual_altered_ninths.ostf` |

**Limits:** Valid examples do not replace negative tests, MusicXML/DAW interoperability testing, or every meter/tempo combination. Run the automated test suite for invalid-input coverage.
