# Maintaining this repository

This repository distributes one agent skill, `skills/amnat-reproducibility/`, in
the shared `SKILL.md` format read by both Claude Code and Codex. Keep it working in
both: plain Markdown, YAML frontmatter with only `name` and `description`, and no
tool-specific features in the skill body.

- `references/amnat-checklist.md` follows the journal's published checklist. Do not
  add requirements the journal does not state; put best-practice advice in other
  references and mark it as a recommendation.
- Guidance beyond the published checklist (privacy, sensitive data, figures not made
  by code, point-and-click analyses) lives in `references/data-editor-guidance.md`,
  with its own IDs (`PRIV`, `SENS`, `FIG`, `GUI`).
- Item IDs (`DOC-1`, `CODE-2`, `GUI-1`, ...) are used in `SKILL.md`, the
  references, and `scripts/audit_archive.py` (including its report sort order).
  Keep them in sync when editing.
- `scripts/audit_archive.py` must use only the Python standard library, so authors
  can run it without installing anything.
- After changing a script, run `python3 tests/test_audit.py`, and add a test
  project or expectation for any new check. Test projects must be made up: never
  copy an author's real data or manuscript into `tests/`.
