# Claude Code Instructions

This repository packages Android finance coding specs as an installable AI skill. Before generating, editing, or reviewing code, read:

- `specs/finance-number-skill.md`
- `specs/rtl-adaption.md`
- `specs/kotlin-style.md`

All MUST and MUST NOT rules are mandatory. Existing repository structure and tooling take priority over generic advice.

When changing specs, run `python3 scripts/sync_skill_refs.py` to update the bundled skill references.
When changing the scanner or examples, run `python3 -m unittest tests/test_android_finance_scan.py`.
