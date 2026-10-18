# OSTF v1.2 — Core Music Interchange Specification

Status: **Version 1.2 — Stable Core**, 2026-10-18. Normative core specification. Independent DAW interoperability and general v1.1 compatibility are not certified.

## 1. Scope
OSTF is a **musical structure, timeline, and harmonic-context interchange format**. It describes the song structure, meter changes, tempo changes, key/scale contexts, and time-positioned chord symbols. It deliberately does **not** prescribe the UI or the way any program edits or renders information.

Excluded: UI state, selection, zoom, viewport, commands, undo history, MIDI notes/numbers, velocity, CC, pitch bend, articulation, voicing/registrations, instruments, plug-in state, audio or audio warp, generation algorithms, and proprietary DAW edit states. A chord root and bass are theoretical pitch classes/spellings, not played notes.

The requirements words **MUST**, **MUST NOT**, **SHOULD**, and **MAY** are normative for implementations declaring v1.2 compatibility.

## 2. Envelope and versioning
- Top-level `format` MUST equal `OSTF`; `version` MUST equal `1.2`.
- `timeBase` MUST be `quarter-note`; all positions and durations are exact nonnegative rational quantities of whole quarter notes, encoded as canonical strings `n` or `n/d` (integer n >= 0, denominator d > 0, reduced to lowest terms). All numerators are nonnegative; durations MUST be strictly positive.
- Song length is `duration`; all interval events MUST fit within `[0,duration)`; point events MAY be at `duration` only where explicitly allowed (none in v1.2).
- Applications MUST reject invalid or unknown required semantic values rather than silently reinterpret them. Unknown top-level fields MAY be preserved for roundtrip but MUST NOT change normative interpretation. Reserved extension container `extensions` is optional; extensions MUST NOT contradict core values.

## 3. Timeline and boundaries
- Position `0` is the beginning of the musical work (not DAW bar offset). An event interval is **half-open** `[start, start+duration)`; neighboring intervals may share boundaries without overlap.
- A quarter note is 1, eighth note is 1/2, 16th note is 1/4, and a triplet eighth note is 1/3. The position of any section, harmony event, tempo event or meter event refers to this single axis. No PPQ is prescribed.
- Events sharing a boundary become effective *at* that boundary; previous events end immediately before it. Event order in arrays is not significant; importers MUST sort by position and reject conflicting duplicate changes at one location.
- `duration` is explicitly stored; modifying meter does not implicitly move stored chord/section positions. Editors decide how to reflow such edits and then write valid OSTF results.

## 4. Meter map and derived bars
- `meterMap` MUST have an initial event at 0. Each event has `at`, `numerator` (positive integer), `denominator` (power of 2 between 1 and 128 inclusive). The signature stays in force up to the next meter event.
- The mathematical duration of a complete measure is `numerator * 4 / denominator` quarter notes (thus 6/8 = 3 quarter notes). This is NOT a definition of perceived beat grouping: 6/8 typically has two dotted-quarter beats. Optional `beatGroups` is an array of positive integer denominator-units summing exactly to `numerator` (e.g. 7/8 as `[2,2,3]`, 6/8 as `[3,3]`). It conveys notated grouping, not a change of meter duration. If absent, grouping is unspecified.
- The first measure begins at 0 unless `song.pickupDuration` is set. With a pickup, the first measure is a partial measure of exactly `pickupDuration` quarter notes beginning at 0, and the next full measure starts at `pickupDuration`. The pickup MUST be shorter than the full measure under the meter effective at 0. A meter change inside the pickup is invalid.  Subsequent measure boundaries are generated sequentially from the current meter. A meter change at a boundary begins a measure of the new meter. A meter change inside a measure closes the preceding measure as a **partial measure** at the change point and begins a new measure there. A song end inside a measure likewise leaves a final partial measure. An application's display of bar numbering is not normative.
- Meter changes MAY occur at any rational position. A consumer that cannot represent mid-measure changes MUST report loss/unsupported conversion rather than silently shift it.
- Sections do not store their own second meter. A meter at a section start is an ordinary meter-map event. Sections do not implicitly restore an earlier meter at their end.

## 5. Tempo map
- `tempoMap` MUST start at 0 and be strictly ordered by position (order in arrays not important).
- Every tempo event stores `bpm` as a positive decimal number and `beatUnit` as a positive rational **whole-note** duration (e.g. `1/4` for quarter-note, `3/8` for dotted quarter); this states exactly what the BPM counts.
- The `transition` field is `step` or `linear-quarter-bpm`. For `step`, the stated tempo applies immediately and remains constant until the next event. For `linear-quarter-bpm`, the instantaneous **quarter-note BPM** interpolates linearly in musical position from the event at `at=a` to the next event at `at=b`; endpoints are `q0=bpm0 * (4 * beatUnit0)` and `q1=bpm1 * (4 * beatUnit1)`, where beat units are whole-note fractions. Thus `q(x)=q0+(q1-q0)*(x-a)/(b-a)` for a <= x < b. `linear-quarter-bpm` MUST have a subsequent tempo event; `b>a` and both endpoint quarter-note BPM values MUST be positive. The last event MUST be `step`.
- For step intervals, elapsed seconds over `L` quarter notes is `60*L/q0`. For a linear segment from x=a to x=a+L, with slope `m=(q1-q0)/(b-a)`, elapsed seconds is `60/m * ln((q0+m*L)/q0)` when m != 0, otherwise `60*L/q0`. This definition deliberately operates in score-time, not wall-clock time; output formats unable to represent it MUST flag a lossy conversion. Floating-point accuracy of rendered seconds is implementation-dependent; event positions remain exact rationals.
- `bpm` is measured per `beatUnit` whole-note duration; thus quarter-note BPM is `bpm * 4 * beatUnit`. A 6/8 bar at dotted-quarter 80 BPM lasts 1.5 seconds.


## 6. Song structure
- `sections` contains named, interval-valued structural spans (`id`, `name`, `start`, `duration`). IDs MUST be unique. Section spans MUST be within the song and MUST NOT overlap in v1.2; gaps are allowed. Sections MAY begin/end between bar lines and MAY coincide with meter/tempo/key/chord boundaries.
- `name` is free text (Verse, Chorus, Intro etc.) and is not an instruction. A section's name or boundaries never changes tempo or meter by itself.

## 7. Key/scale map
- `keyMap` MAY contain harmonic-context events, each at `at` with `tonic` as a spelled pitch class (`C`, `F#`, `Bb`), and `scale` as a recognized scale identifier such as `major`, `natural-minor`, `dorian`, `mixolydian`, or an optional extension-defined identifier. For the Core v1.2 schema, the listed built-in IDs are authoritative; additional built-in IDs in v1.2 include pentatonic, blues, whole-tone, octatonic, chromatic, harmonic-major, lydian-dominant, altered and phrygian-dominant. A scale ID identifies a conventional theoretical collection, NOT a MIDI pitch sequence or voicing. Core 12-TET pitch-class mappings and spelling preservation are specified in Section 10; full note-name spelling of collections is not standardized.
- Key contexts persist until the next key event. An absent `keyMap` means no key was asserted, not C major. A key is not a forced restriction on the chords that occur.

## 8. Chord timeline and symbols
- Each `chords` entry describes a harmonic span (`start`, `duration`, `kind`). `kind="chord"` requires `root` (spelled pitch class) and `quality` (standard enumerated harmonic quality), optional `bass` (spelled pitch class), `degrees` (harmonic additions/alterations/omissions), and optional `symbol` (display label only). `kind="no-chord"` means an explicit N.C. span and MUST NOT carry chord-definition fields.
- A missing harmony span signifies **unspecified/unknown harmony**, not N.C. The source of truth is normalized semantic fields, not the display label. Programs MUST NOT infer played notes, octaves, or MIDI velocities from the core representation.
- Chords in v1.2 MUST NOT overlap; at a time there is at most one asserted chord context. For true polyharmony, a later extension may define distinct harmony layers.
- The `quality` core vocabulary is `major`, `minor`, `diminished`, `augmented`, `sus2`, `sus4`, `dominant-seventh`, `major-seventh`, `minor-seventh`, `half-diminished-seventh`, `diminished-seventh`, `minor-major-seventh`. v1.2 additionally admits power, sixth, six-nine, ninth, eleventh, thirteenth, augmented-seventh and dominant-sus4 quality names as explicitly enumerated by the schema. Their abstract degree/semitone definitions are now listed in the v1.2 normative registry (Section 10).
- `degrees` items use the integer `degree` (2–13), `alter` (integer -2..2 semitones relative to diatonic degree), `operation` one of `add`, `alter`, `omit`; duplicate degree transformations are forbidden. v1.2 defines `add` as an asserted additional scale degree, `omit` as a degree absent from the abstract chord structure, and `alter` as replacement of the unaltered indicated degree with its altered form. Alterations are in 12-TET semitones relative to the diatonic interval named by the degree. v1.2 supplies quality-specific defaults and operation semantics in Section 10; simultaneous variants are represented with `additionalTones`. Chord semantics MUST NOT be guessed from `symbol`.
- Pitch spelling MAY use standard letters A-G followed by at most one `b` or `#` in v1.2. Double accidentals and microtonal pitch systems require future scope.

## 9. Validation and interoperability
- JSON Schema provides the **syntactic contract**. Cross-field requirements (map beginnings, strict chronology, exact rational arithmetic, overlaps, boundaries, degree duplicates) are the **semantic contract** and MUST also be checked.
- A conforming reader MUST give identical musical positions and meanings for all valid v1.2 core records, or explicitly flag an unsupported feature. A writer MUST serialize a self-consistent document. Data conversion into MusicXML, SMF, DAWproject, or DAW APIs is an adapter task, not automatic compatibility.
- Producers MUST preserve the distinction between an absent value and an explicitly specified value. Exporters SHOULD report loss of expressiveness (e.g. tempo ramps, unsupported chord extensions, partial bars).

## 10. Normative harmony registry
`OSTF_v1.2_harmony_registry.json` is normative for v1.2 and defines 25 chord qualities and 20 built-in scales as 12-TET theoretical interval structures. It is not MIDI note data. Consumers MUST reject unknown core identifiers. `melodic-minor` is ascending jazz melodic minor; `blues` is minor-blues hexatonic; `altered` is the seven-note super-Locrian collection.

Pitch names `A`..`G` with optional `b` or `#` encode **spelled pitch classes**, not octave pitches. Pitch-class equivalence uses A=9, B=11, C=0, D=2, E=4, F=5, G=7 modulo 12, with accidentals +/-1. Importers MUST preserve the supplied spelling (e.g. `C#` versus `Db`); equivalence of sound does not authorize changing a displayed spelling. Quality interval spellings are defined by the registry degree numbers, whereas scale registry entries specify pitch-class collections without an obligatory note-letter spelling. This distinction is deliberate; full key-dependent enharmonic rendering remains adapter behavior.

A chord quality supplies a set of `(degree, semitones)` pairs. Degree 1 is the root and MUST remain present. Degree labels distinguish harmonic function, including octave-equivalent degrees (e.g. 2 versus 9); semitone offsets are measured upward from the root for *abstract definition only*. An optional slash `bass` is an independent pitch-class spelling and MUST NOT imply any physical octave, voice, or MIDI note. It MAY be outside the chord's collection.

The `degrees` array modifies the quality's abstract degree map. Each degree can occur **at most once across all operations** (one operation per degree). Degree names 2..13 use the major-scale reference offsets `{2:2,3:4,4:5,5:7,6:9,7:11,8:12,9:14,10:16,11:17,12:19,13:21}` semitones.

- `add`: degree MUST NOT yet exist; insert `majorReference[degree] + alter`.
- `alter`: degree MUST exist; replace its offset with `majorReference[degree] + alter`, **not** a semitone increment on its current offset.
- `omit`: degree MUST exist; `alter` MUST be zero; remove that degree.

This means `minor` quality already has b3, and `alter` of degree 3 with `alter=-1` still yields b3. `C7(b9)` can be encoded using `dominant-seventh` plus `add(9,-1)`. Simultaneous b9 and #9 are represented by `additionalTones`.


## 11. Simultaneous harmonic tone variants
A `kind: chord` event MAY have `additionalTones`, an array of `{degree, alter}` objects where degree is 2..13 and alter is an integer semitone displacement -2..2 relative to the major-reference interval defined in Section 10. These are **abstract harmonic components**, not MIDI pitches, registers or voicings. They supplement the effective degree map after applying `degrees` operations; they do not replace or mutate any existing degree.

For example, G7(b9,#9) MAY be encoded as `quality: dominant-seventh` and `additionalTones: [{degree:9,alter:-1},{degree:9,alter:1}]`. After applying normal `degrees`, the result is a **multiset indexed by both degree and semitone offset** (the same degree may occur with two different semitone offsets). A duplicate `(degree,semitone-offset)` pair MUST be rejected, even when one member came from the base quality or `degrees`. Order of entries in `additionalTones` has no semantic significance. The root (degree 1) MUST NOT be inserted via `additionalTones`. Core chord symbol text remains informational; it never supersedes the structured fields.

Other implications: the value of `degrees` continues to permit at most one transformation per *degree*; simultaneous variants belong only in `additionalTones`. An explicit unaltered 9 and added b9 can coexist if the two semitone offsets differ. This feature extends Draft 3 without changing existing valid Draft 3 documents.


## 12. Conformance and compatibility
- **Producer**: MUST emit JSON satisfying the schema and all semantic checks; MUST preserve canonical rational times; MUST NOT silently convert unsupported chord qualities or beat units.
- **Consumer**: MUST respect half-open spans, effective-at-boundary changes, and the distinction between unspecified harmony and explicit N.C.; MUST reject unsupported normative values instead of silently substituting them.
- **Roundtrip writer**: MUST preserve all defined musical semantics including pitch-class spelling, duration, time coordinates, maps and chord components; array ordering is non-semantic.
- **Loss reporting**: every lossy adapter MUST identify affected data, the conversion limitation and whether output was produced. Unsupported mapping is not evidence of interoperability.
- **Compatibility**: official v1.1 files have not been compared with an authoritative v1.1 standard; NO general v1.1 compatibility claim is made. The provided v1.1 editor *preview* converter is experimental. MusicXML and third-party DAW interoperability is not implemented or claimed.
- **Scope**: MIDI performed notes, CC, velocity, voicing, audio, UI state and editor commands remain outside core. 

## 13. Publication status
This document defines **OSTF v1.2 Stable Core**. The fixed core baseline consists of this normative specification, `OSTF_v1.2.schema.json`, `OSTF_v1.2_harmony_registry.json`, and the semantic validation invariants. Any incompatible semantics require a future version. Publication of the core format does not certify any external adapter, prior-version lossless migration, or particular application implementation. See `COMPATIBILITY.md` in the package root.
