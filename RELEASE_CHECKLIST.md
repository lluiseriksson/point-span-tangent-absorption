# Local release gate (not published)

External publication is intentionally disabled for this draft.  A later
instruction said not to publish to ARR, and the current workspace is not a
Git repository, so there is no legitimate remote, branch, PR, CI run, tag, or
release to mutate.

Before any future publication, all of the following should be true:

- [x] Independent adversarial mathematical review completed and archived.
- [x] Every accepted correction incorporated into `manuscript.tex`.
- [x] pdfLaTeX succeeds on at least two passes.
- [x] Final log has no errors, warnings, undefined references/citations, or
  overfull/underfull boxes.
- [x] Every page rendered and visually inspected.
- [x] Exact finite replays pass with their scope limitation stated.
- [x] SHA-256 manifest and deterministic ZIP verify.
- [ ] User resolves the conflict and explicitly authorizes ARR publication.
- [ ] A named Git remote/repository and target branch are supplied or created
  under explicit authority.
- [ ] CI runs on that exact commit and passes.
- [ ] PR review is completed on the exact commit.
- [ ] Release tag, archive, and public record all point to the same hashes.
- [ ] Any license is supplied or explicitly selected by the rights holder.

Until the unchecked authority and infrastructure gates are satisfied, this is
a local research artifact only.
