# Android Finance Spec Agent Instructions

When generating, editing, reviewing, or refactoring this repository, follow all Android finance specs:

- `specs/finance-number-skill.md`
- `specs/rtl-adaption.md`
- `specs/kotlin-style.md`

Rules:

1. Treat every MUST and MUST NOT rule as a hard gate.
2. Keep the installable skill in `skills/android-finance-spec/` synchronized with root `specs/`.
3. Before adding code, search for existing structure, naming, scripts, and documentation patterns.
4. Do not invent missing helpers, wrappers, base classes, abstractions, or dependencies.
5. After changing specs, run `python3 scripts/sync_skill_refs.py`.
6. After changing scanner logic or examples, run `python3 -m unittest tests/test_android_finance_scan.py`.
