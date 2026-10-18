# OSTF v1.2 — Parameter Reference Manual (English)

This is a field-by-field reference for **OSTF v1.2 Stable Core**. Normative requirements are in `spec/OSTF_v1.2_Core_Specification.md`; schema and harmony registry take precedence over this explanation if wording differs.

## Data fields

| JSON path | Type / allowed values | Required | Musical meaning |
|---|---|---|---|
| `format` | string (const OSTF) | Yes | Format identifier. |
| `version` | string (const 1.2) | Yes | Format version; not app version. |
| `timeBase` | string (const quarter-note) | Yes | One quarter-note is timeline unit 1. |
| `duration` | positive canonical rational string | Yes | Total musical duration measured in quarter notes. |
| `song` | object | No | Musical work metadata only. |
| `song.title` | string | No | Human-readable title; Unicode is supported. |
| `song.pickupDuration` | positive rational | No | Short initial partial measure, shorter than initial full bar. |
| `meterMap` | array | Yes | Ordered-by-time meter change events; must include at 0. |
| `meterMap[].at` | rational | Yes | Event position |
| `meterMap[].numerator` | positive integer | Yes | Time-signature numerator |
| `meterMap[].denominator` | 1/2/4/8/16/32/64/128 | Yes | Time-signature denominator |
| `meterMap[].beatGroups` | positive integer array | No | Optional notated grouping; sum must equal numerator |
| `tempoMap` | array | Yes | Tempo event sequence, starting at 0. |
| `tempoMap[].at` | rational | Yes | Event position |
| `tempoMap[].bpm` | positive number | Yes | Beat-unit counts per minute |
| `tempoMap[].beatUnit` | positive rational (whole-note fraction) | Yes | Duration of metronome beat; 1/4 quarter, 3/8 dotted-quarter |
| `tempoMap[].transition` | step | linear-quarter-bpm | Yes | Transition to next event; last must be step |
| `keyMap` | array | No | Key/scale context changes; absence does not imply C major. |
| `keyMap[].at` | rational | Yes | Context begins at this position |
| `keyMap[].tonic` | spelled pitch class | Yes | A–G with optional b or # |
| `keyMap[].scale` | 20-ID enum | Yes | Built-in scale ID from normative registry |
| `sections` | array | Yes | Nonoverlapping musical form sections; gaps allowed. |
| `sections[].id` | nonempty string | Yes | Unique stable identifier |
| `sections[].name` | string | Yes | Section label, Unicode |
| `sections[].start` | rational | Yes | Section absolute onset |
| `sections[].duration` | positive rational | Yes | Section interval length |
| `chords` | array | Yes | Nonoverlapping harmony spans; absent span is unknown harmony. |
| `chords[].kind` | chord | no-chord | Yes | Explicit N.C. versus chord |
| `chords[].start` | rational | Yes | Onset |
| `chords[].duration` | positive rational | Yes | Length |
| `chords[].root` | spelled pitch class | Conditional/No | Required for kind=chord |
| `chords[].quality` | 25-ID enum | Conditional/No | Required for kind=chord |
| `chords[].bass` | spelled pitch class | Conditional/No | Slash bass theoretical pitch spelling |
| `chords[].symbol` | string | Conditional/No | Optional display label only; not semantic authority |
| `chords[].degrees` | array | Conditional/No | Abstract per-degree modifications |
| `chords[].additionalTones` | array | Conditional/No | Simultaneous altered tone variants |
| `chords[].degrees[].degree` | integer 2..13 | Yes | Harmonic degree number |
| `chords[].degrees[].alter` | integer -2..2 | Yes | Chromatic deviation vs major-scale interval |
| `chords[].degrees[].operation` | add | alter | omit | Yes | Modification operation |
| `chords[].additionalTones[].degree` | integer 2..13 | Yes | Additional harmonic degree |
| `chords[].additionalTones[].alter` | integer -2..2 | Yes | Deviation vs major reference |
| `extensions` | object | No | Non-conflicting vendor extensions; no impact on core semantics. |

## Interpretative rules

- All position/duration rational strings must be reduced (`0`, `3/2`, `7`); no decimals or `2/4`.
- Event intervals are half-open; same-boundary events apply at their `at`/`start` location.
- Meter bar length = `numerator × 4 / denominator` quarter-note units. Meter events may interrupt bars; sections never automatically restore an earlier meter.
- For `linear-quarter-bpm`, quarter BPM interpolates with **score position**, not elapsed seconds. Convert beat-unit BPM as `bpm × 4 × beatUnit`.
- `degrees` transforms a chord's abstract degree map. `add` inserts absent, `alter` replaces existing, `omit` removes existing. `additionalTones` allows same-degree different accidental variants.
- The chord root must remain present. No pitch fields imply note octave, velocity, MIDI, voicing, instrument, or playback.
- A gap in `chords` denotes unspecified harmony; `kind=no-chord` asserts an explicit N.C.
- JSON Schema validates field shapes; use `tests/validate_ostf.py` to check cross-field invariants.
- Arrays of event changes are semantically sorted by their positions; conflicting simultaneous changes are invalid.

## Chord quality identifiers (25)

| Identifier | Theoretical degree:semitone pairs |
|---|---|
| `major` | 1:0, 3:4, 5:7 |
| `minor` | 1:0, 3:3, 5:7 |
| `diminished` | 1:0, 3:3, 5:6 |
| `augmented` | 1:0, 3:4, 5:8 |
| `sus2` | 1:0, 2:2, 5:7 |
| `sus4` | 1:0, 4:5, 5:7 |
| `dominant-seventh` | 1:0, 3:4, 5:7, 7:10 |
| `major-seventh` | 1:0, 3:4, 5:7, 7:11 |
| `minor-seventh` | 1:0, 3:3, 5:7, 7:10 |
| `half-diminished-seventh` | 1:0, 3:3, 5:6, 7:10 |
| `diminished-seventh` | 1:0, 3:3, 5:6, 7:9 |
| `minor-major-seventh` | 1:0, 3:3, 5:7, 7:11 |
| `power` | 1:0, 5:7 |
| `dominant-ninth` | 1:0, 3:4, 5:7, 7:10, 9:14 |
| `major-ninth` | 1:0, 3:4, 5:7, 7:11, 9:14 |
| `minor-ninth` | 1:0, 3:3, 5:7, 7:10, 9:14 |
| `dominant-eleventh` | 1:0, 3:4, 5:7, 7:10, 9:14, 11:17 |
| `minor-eleventh` | 1:0, 3:3, 5:7, 7:10, 9:14, 11:17 |
| `dominant-thirteenth` | 1:0, 3:4, 5:7, 7:10, 9:14, 11:17, 13:21 |
| `major-sixth` | 1:0, 3:4, 5:7, 6:9 |
| `minor-sixth` | 1:0, 3:3, 5:7, 6:9 |
| `six-nine` | 1:0, 3:4, 5:7, 6:9, 9:14 |
| `minor-six-nine` | 1:0, 3:3, 5:7, 6:9, 9:14 |
| `augmented-seventh` | 1:0, 3:4, 5:8, 7:10 |
| `dominant-sus4` | 1:0, 4:5, 5:7, 7:10 |

## Scale identifiers (20)

| Identifier | Theoretical pitch-class interval values |
|---|---|
| `major` | `[0, 2, 4, 5, 7, 9, 11]` |
| `natural-minor` | `[0, 2, 3, 5, 7, 8, 10]` |
| `dorian` | `[0, 2, 3, 5, 7, 9, 10]` |
| `mixolydian` | `[0, 2, 4, 5, 7, 9, 10]` |
| `phrygian` | `[0, 1, 3, 5, 7, 8, 10]` |
| `lydian` | `[0, 2, 4, 6, 7, 9, 11]` |
| `locrian` | `[0, 1, 3, 5, 6, 8, 10]` |
| `harmonic-minor` | `[0, 2, 3, 5, 7, 8, 11]` |
| `melodic-minor` | `[0, 2, 3, 5, 7, 9, 11]` |
| `major-pentatonic` | `[0, 2, 4, 7, 9]` |
| `minor-pentatonic` | `[0, 3, 5, 7, 10]` |
| `blues` | `[0, 3, 5, 6, 7, 10]` |
| `whole-tone` | `[0, 2, 4, 6, 8, 10]` |
| `octatonic-whole-half` | `[0, 2, 3, 5, 6, 8, 9, 11]` |
| `octatonic-half-whole` | `[0, 1, 3, 4, 6, 7, 9, 10]` |
| `chromatic` | `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]` |
| `harmonic-major` | `[0, 2, 4, 5, 7, 8, 11]` |
| `lydian-dominant` | `[0, 2, 4, 6, 7, 9, 10]` |
| `altered` | `[0, 1, 3, 4, 6, 8, 10]` |
| `phrygian-dominant` | `[0, 1, 4, 5, 7, 8, 10]` |

## Coverage and interoperability

`docs/EXAMPLE_COVERAGE.md` maps the format requirements to `.ostf` examples. Samples are **interchange documents**, not MIDI or playable scores. Country-specific language is confined to Unicode song/section labels and translated guides; internationally stable JSON field names remain English.

Version 1.1 universal lossless interchange, MusicXML roundtrips and third-party DAW interoperability are **not certified**. See `COMPATIBILITY.md`.
