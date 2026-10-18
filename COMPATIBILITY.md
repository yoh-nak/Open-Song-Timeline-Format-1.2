# OSTF v1.2 Stable Core — Compatibility Declaration

- **Supported internal claim:** supplied v1.2 examples pass included structural and semantic reference validation; internal timing, harmony and normalization tests pass in the documented environment.
- **Not claimed:** all v1.1 files are compatible, v1.1 -> v1.2 migration is lossless, a specific DAW supports the format, MusicXML roundtrips are accurate, or Lead Sheet Editor / Music Studio already implement v1.2.
- The provided `tools/migrate_v11_preview.py` handles a limited **experimental editor 1.1 preview** subset only; it reports unconvertible or assumed data. Preserve the source.
- Third-party support requires a separately developed adapter, test vectors and explicit capability declaration. Unrecognized content must not be silently converted.
- A stable core release means the interchange meaning is frozen, **not** that all external products interoperate.
