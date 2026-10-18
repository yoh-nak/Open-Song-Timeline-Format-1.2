# OSTF v1.2 Core Conformance

A **producer** MUST satisfy the JSON Schema and semantic constraints in the core specification, including canonical rational strings, valid interval bounds, consistent non-overlap, explicit map-change positions and structured chord semantics.

A **consumer** MUST respect the same time axis and half-open events, preserve pitch spelling, distinguish unspecified harmony from explicit N.C., reject unsupported normative values or state a capability limit, and must not invent MIDI notes or UI state.

A **roundtrip writer** MUST preserve musical semantics or issue a loss report identifying each unsupported field or conversion. Reordering arrays of changes is not a semantic change. Chord `symbol` is a label, never an override of theoretical components.

**Conformance is demonstrated per implementation**, not inherited just by recognizing a file extension. The included validator is a reference implementation rather than an independent interoperability certification.
