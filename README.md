# OSTF v1.2 — Stable Core (GitHub distribution)

**Open music-structure interchange format**: common quarter-note rational timeline for meter, tempo, sections, key/scale and theoretical chord progression.

This is a **format specification**, not a DAW plugin. Files ending in `.ostf` contain UTF-8 JSON and follow the published JSON Schema plus semantic constraints. No MIDI performance events, sound, audio, voicing, UI settings or software-specific controls.

## Quick start

1. Open `examples/01_international_song.ostf` in a text editor to inspect the self-describing JSON fields.
2. Install Python 3.10+ and `pip install -r requirements.txt`.
3. Run `python tests/validate_ostf.py examples/01_international_song.ostf` or `python tests/validate_ostf.py examples/*.ostf` (shell glob expands on macOS/Linux; on Windows PowerShell use the included `tools/validate_all_examples.py`).
4. Run `python tools/validate_all_examples.py` for all provided `.ostf` examples on any OS.
5. Run the conformance regression suite: `python tools/run_tests.py`.

## Documentation

- [Parameter reference, every defined field](docs/PARAMETER_REFERENCE.md)
- [Comprehensive example coverage](docs/EXAMPLE_COVERAGE.md)
- [Expanded sample catalog (49 examples)](docs/SAMPLE_CATALOG.md)
- [Normative core specification](spec/OSTF_v1.2_Core_Specification.md)
- [JSON Schema](spec/OSTF_v1.2.schema.json)
- [Normative chord/scale registry](spec/OSTF_v1.2_harmony_registry.json)
- [Conformance](CONFORMANCE.md) · [Compatibility limitations](COMPATIBILITY.md)

### Translated introductions

日本語 · 简体中文 · 繁體中文 · 한국어 · Español · Français · Deutsch · Português · हिन्दी · العربية: see [docs/i18n](docs/i18n). English normative field identifiers and specifications are shared by all translations.

## Publication / GitHub web upload

Extract the distribution ZIP first, create an empty GitHub repository, choose **Add file → Upload files**, and drag the *contents* of this folder (not the ZIP itself). GitHub's browser upload file-count restrictions vary; the package is deliberately below 100 files. Git or GitHub Desktop can be used if folder upload is inconvenient. Review `GITHUB_PUBLISHING.md` before publishing.

## Guarantees and caveats

This is the **Stable Core v1.2** standard with a verified reference validator and sample fixtures. Neither complete OSTF v1.1 migration nor MusicXML/third-party DAW interoperability is certified. Avoid claiming such compatibility until tested.
