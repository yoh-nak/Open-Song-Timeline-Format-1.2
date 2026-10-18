# OSTF v1.2 sample catalog / サンプル一覧

49 `.ostf` example files; 36 additional focused examples. All example content is JSON encoded in UTF-8.

## How to use / 使用方法

Run `python tools/validate_all_examples.py` from the extracted repository. Each example illustrates a specific valid format case; it is not an audio recording or a MIDI file.

## New focused examples

| File | Musical situation explained in English |
|---|---|
| `10_minimal_empty_timeline.ostf` | Minimal valid OSTF with no harmony |
| `11_basic_c_major_progression.ostf` | Four chords in C major |
| `12_two_chords_per_bar.ostf` | Two chord changes per 4/4 bar |
| `13_one_three_four_meter.ostf` | One three four and five four sections |
| `14_common_compound_meter.ostf` | Six eight compound feel |
| `15_additive_seven_eight.ostf` | Seven eight grouped 2+2+3 |
| `16_additive_eleven_eight.ostf` | Eleven eight grouped 3+3+3+2 |
| `17_additive_fifteen_sixteen.ostf` | Fifteen sixteen grouped 4+4+4+3 |
| `18_meter_change_at_section.ostf` | Meter changes aligned to sections |
| `19_meter_change_inside_section.ostf` | Meter changes inside a single section |
| `20_meter_change_mid_bar.ostf` | Interrupted bar at non-boundary |
| `21_pick_up_one_beat.ostf` | One quarter note anacrusis |
| `22_pick_up_eighth_note.ostf` | Eighth note anacrusis |
| `23_tempo_step_changes.ostf` | Instantaneous tempo changes |
| `24_tempo_accelerando.ostf` | Accelerando and steady tempo |
| `25_tempo_ritardando.ostf` | Ritardando and steady tempo |
| `26_tempo_multiphase.ostf` | Multiple ramps and discrete tempo change |
| `27_half_note_beat_unit.ostf` | Half-note BPM reference unit |
| `28_eighth_note_beat_unit.ostf` | Eighth-note BPM reference unit |
| `29_key_modulation.ostf` | Major key modulation from C to E |
| `30_modal_changes.ostf` | Modal color changes |
| `31_enharmonic_spelling.ostf` | Preserving sharp and flat spelling |
| `32_slash_chords.ostf` | Chord slash bass as theoretical harmony |
| `33_sus_and_power_chords.ostf` | Suspended and power chord qualities |
| `34_jazz_ii_v_i.ostf` | Jazz ii V I with extensions |
| `35_altered_dominants.ostf` | Distinct dominant alteration examples |
| `36_add_ninth.ostf` | Added ninth on a triad |
| `37_omit_fifth.ostf` | Fifth omitted from major seventh chord |
| `38_alter_fifth.ostf` | Altered fifth in dominant seventh |
| `39_no_chord_vs_unspecified.ostf` | Explicit no chord versus no harmony data |
| `40_rational_septuplets.ostf` | Exact septuplet-like onset without integer PPQ |
| `41_section_names_unicode.ostf` | Unicode song and section labels |
| `42_section_gaps.ostf` | Sections with intentional uncovered time |
| `43_full_song_integration.ostf` | Complete song integration: meter tempo modulations chords |
| `44_vendor_extension_ignored.ostf` | Optional vendor metadata that cannot alter musical meaning |
| `45_thirty_two_note_meter.ostf` | Thirty-second denominator and 9/32 grouping |

## Original examples

See `docs/EXAMPLE_COVERAGE.md` for the existing 13 examples.

## Interpretation notes

- All time positions use exact quarter-note-based rational coordinates, not MIDI ticks.
- A `no-chord` event is explicit; a gap in `chords` is unspecified harmony.
- Sections are musical ranges; meter changes are defined only by `meterMap`.
- Software UI settings, audio and MIDI performance notes are outside the format.
- These are representative valid examples; interoperability with specific DAWs remains unverified.
