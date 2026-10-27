# Maintaining this repository

This repository distributes one agent skill, `skills/amnat-reproducibility/`, in
the shared `SKILL.md` format read by both Claude Code and Codex. Keep it working in
both: plain Markdown, YAML frontmatter with only `name` and `description`, and no
tool-specific features in the skill body.

- `references/amnat-checklist.md` follows the journal's published checklist. Do not
  add requirements the journal does not state; put best-practice advice in other
  references and mark it as a recommendation.
- Item IDs (`DOC-1`, `CODE-2`, ...) are used in `SKILL.md`, `long-computations.md`,
  and `scripts/audit_archive.py`. Keep them in sync when editing.
- `scripts/audit_archive.py` must use only the Python standard library, so authors
  can run it without installing anything.
- After changing the script, run it on a small test project containing the
  problems it should catch, and on a clean one, and check the report.
