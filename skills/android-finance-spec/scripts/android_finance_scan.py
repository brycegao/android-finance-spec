#!/usr/bin/env python3
"""Static first-pass scanner for Android finance AI specs."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


SKIP_DIRS = {
    ".git",
    ".gradle",
    ".idea",
    ".kotlin",
    "build",
    "node_modules",
    "out",
}

TEXT_EXTS = {".kt", ".java", ".xml"}


@dataclass
class Finding:
    severity: str
    code: str
    path: Path
    line: int
    message: str
    snippet: str


RULES: list[tuple[str, str, set[str], re.Pattern[str], str]] = [
    (
        "P1",
        "FIN_FLOATING_DECIMAL_FIELD",
        {".kt", ".java"},
        re.compile(
            r"\b(amount|price|balance|fee|rate|ratio|profit|loss|pnl|margin|quantity|qty|volume)\w*"
            r"\s*:\s*(Double|Float)\??",
            re.IGNORECASE,
        ),
        "Financial decimal-looking field uses Double/Float; use String or BigDecimal.",
    ),
    (
        "P1",
        "FIN_TO_DOUBLE_FLOAT",
        {".kt", ".java"},
        re.compile(r"\.to(Double|Float)\s*\("),
        "Financial code must not convert values through Double/Float.",
    ),
    (
        "P1",
        "FIN_BIGDECIMAL_FLOATING_CTOR",
        {".kt", ".java"},
        re.compile(r"\bBigDecimal\s*\(\s*[^\"']"),
        "Check BigDecimal constructor; prefer string/valueOf-safe sources, never floating values.",
    ),
    (
        "P1",
        "FIN_BIGDECIMAL_TOSTRING",
        {".kt", ".java"},
        re.compile(
            r"\bBigDecimal\b.*\.toString\s*\(\)",
        ),
        "BigDecimal must use toPlainString(), not toString(), to avoid scientific notation.",
    ),
    (
        "P2",
        "FIN_MANUAL_FORMAT",
        {".kt", ".java"},
        re.compile(r"\b(String\.format|DecimalFormat)\b"),
        "Financial display should use the project's NumericFormat or equivalent formatter.",
    ),
    (
        "P1",
        "RTL_LEFT_RIGHT_XML",
        {".xml"},
        re.compile(
            r"(layout_constraintLeft|layout_constraintRight|layout_marginLeft|layout_marginRight|"
            r"paddingLeft|paddingRight|drawableLeft|drawableRight|gravity=\"left\"|gravity=\"right\"|"
            r"textAlignment=\"viewLeft\"|textAlignment=\"viewRight\")"
        ),
        "Use start/end-aware attributes instead of left/right.",
    ),
    (
        "P2",
        "RTL_LAYOUT_DIRECTION",
        {".xml"},
        re.compile(r"layoutDirection=\"(rtl|ltr)\""),
        "layoutDirection needs a fixed-direction business reason and a comment.",
    ),
    (
        "P1",
        "I18N_HARDCODED_ANDROID_TEXT",
        {".xml"},
        re.compile(r"android:text=\"(?!@string/|@\{|@android:|\\@|\?attr/|%s|%1\$s)([^\"]*[A-Za-z\u4e00-\u9fff][^\"]*)\""),
        "Visible XML text should use @string resources.",
    ),
    (
        "P2",
        "KOTLIN_NOT_NULL_ASSERT",
        {".kt"},
        re.compile(r"(?<=[)\w])!!"),
        "Avoid Kotlin non-null assertions in production code.",
    ),
    (
        "P1",
        "KOTLIN_GLOBAL_SCOPE",
        {".kt", ".java"},
        re.compile(r"\bGlobalScope\b"),
        "GlobalScope is forbidden; use lifecycle-aware scopes.",
    ),
]


def iter_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix in TEXT_EXTS:
            files.append(path)
    return sorted(files)


def scan_file(root: Path, path: Path) -> list[Finding]:
    findings: list[Finding] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return findings

    for index, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("//"):
            continue
        for severity, code, exts, pattern, message in RULES:
            if path.suffix not in exts:
                continue
            if pattern.search(line):
                findings.append(
                    Finding(
                        severity=severity,
                        code=code,
                        path=path.relative_to(root),
                        line=index,
                        message=message,
                        snippet=stripped[:180],
                    )
                )
    return findings


def render_markdown(findings: list[Finding]) -> str:
    if not findings:
        return "# Android Finance Spec Scan\n\nNo first-pass issues found.\n"

    priority = {"P1": 0, "P2": 1, "P3": 2}
    findings = sorted(findings, key=lambda item: (priority.get(item.severity, 9), str(item.path), item.line))
    lines = [
        "# Android Finance Spec Scan",
        "",
        f"Found {len(findings)} first-pass issue(s).",
        "",
    ]
    for finding in findings:
        lines.extend(
            [
                f"## [{finding.severity}] {finding.code}",
                "",
                f"- Location: `{finding.path}:{finding.line}`",
                f"- Message: {finding.message}",
                f"- Snippet: `{finding.snippet}`",
                "",
            ]
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan an Android project against finance AI coding specs.")
    parser.add_argument("root", nargs="?", default=".", help="Project root to scan.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        raise SystemExit(f"Path does not exist: {root}")

    findings: list[Finding] = []
    for path in iter_files(root):
        findings.extend(scan_file(root, path))

    print(render_markdown(findings))
    return 1 if any(item.severity == "P1" for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
