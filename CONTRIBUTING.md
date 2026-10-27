# Contributing

Rules for editing the skill are in [AGENTS.md](AGENTS.md), which coding agents
working in this repository also read.

## Layout

```text
skills/amnat-reproducibility/
├── SKILL.md                       instructions the agent follows
├── references/
│   ├── amnat-checklist.md         the journal checklist, with item IDs
│   ├── data-editor-guidance.md    privacy, sensitive data, figures, point-and-click
│   └── long-computations.md       Bayesian, simulation, and pipeline guidance
├── scripts/
│   ├── audit_archive.py           automated scan of the archive
│   ├── manuscript_items.py        lists figures, tables, and numbers in the paper
│   └── docx_track_changes.py      applies edits to a Word copy as tracked changes
└── templates/
    ├── README_template.md         README in the journal's required order
    ├── AUTHOR_TODO_template.md    to-do list for authors, kept outside the archive
    ├── codebook_template.csv      variable-level codebook
    └── AGENTS_snippet.md          rules to add to a project's AGENTS.md/CLAUDE.md
docs/quick-start.md                steps and prompts for authors
docs/user-guide.md                 guide for authors
tests/                             made-up projects with planted problems
install.sh                         copies the skill into a project or user folder
```

## Testing

Check the scan after any change to the scripts:

```sh
python3 tests/test_audit.py
python3 tests/test_docx_track_changes.py
```

To test the whole skill, install it into a copy of a test project, run Claude Code
or Codex there, and compare the report with the answer key in
[tests/README.md](tests/README.md). Test projects must be made up; never copy an
author's real data or manuscript into `tests/`.
