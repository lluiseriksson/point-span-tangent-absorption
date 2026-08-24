# Successor draft v0.1

This directory contains a separate successor paper.  It does not overwrite
the source manuscript or the reviewed v0.5 package.

## Contents

- `manuscript.tex`: editable source.
- `paper.pdf`: compiled ten-page paper.
- `paper.txt`: text extracted from the PDF for accessibility and audits.
- `repro/`: exact finite matrix fixtures and package-verification scripts.
- `RESEARCH_AUDIT.md`: claim ledger and public-corpus boundary.
- `REFEREE_REPORT.md`: independent adversarial report (added after review).
- `BUILD_REPORT.json` and `MANIFEST.sha256`: sizes and SHA-256 digests.

## Reproduction

From `repro/` run:

```powershell
python .\run_all_replays.py
python .\verify_successor_fixtures.py --json
```

Compile `manuscript.tex` with pdfLaTeX for at least two passes.  The frozen
PDF was checked for LaTeX errors, warnings, undefined references, and
overfull/underfull boxes, then all ten rendered pages were inspected.

The replays certify only their displayed finite matrices.  The Bertini step,
the universal theorems, novelty, and priority remain mathematical and
literature-review questions rather than computational outputs.

No license is asserted by this package.  No ARR submission, repository push,
PR, release, or public record has been created from this draft.
