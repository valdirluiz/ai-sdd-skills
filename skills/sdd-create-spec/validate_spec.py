#!/usr/bin/env python3
"""
Validates an SDD spec.md to ensure it defines WHAT to build, not HOW.

Usage:
    python validate_spec.py <path-to-spec.md>

Exit codes:
    0  - valid (no errors; warnings may still be present)
    1  - invalid (one or more errors found)
    2  - usage error or file not found
"""

import sys
import re
import json
from pathlib import Path


REQUIRED_SECTIONS = [
    "Overview",
    "Problem Statement",
    "Goals",
    "Non-Goals",
    "Requirements",
    "User Stories",
    "Acceptance Criteria",
]

# Patterns that indicate HOW rather than WHAT
HOW_PATTERNS = [
    (r"\bGET\s+/\S+", "HTTP GET route"),
    (r"\bPOST\s+/\S+", "HTTP POST route"),
    (r"\bPUT\s+/\S+", "HTTP PUT route"),
    (r"\bDELETE\s+/\S+", "HTTP DELETE route"),
    (r"\bPATCH\s+/\S+", "HTTP PATCH route"),
    (r"\bSELECT\s+.+\s+FROM\b", "SQL SELECT statement"),
    (r"\bINSERT\s+INTO\b", "SQL INSERT statement"),
    (r"\bUPDATE\s+\w+\s+SET\b", "SQL UPDATE statement"),
    (r"\bDELETE\s+FROM\b", "SQL DELETE statement"),
    (r"\b(CREATE|DROP|ALTER)\s+TABLE\b", "SQL DDL statement"),
    (r"(?<!\w)(src|lib|app|pkg)/\S+\.\w+", "source file path"),
]

PLACEHOLDER_PATTERNS = [
    (r"^\s*\.\.\.\s*$", "bare ellipsis"),
    (r"\[your (text|content|description|value) here\]", "unfilled bracket placeholder"),
    (r"\bTODO\b", "TODO marker"),
    (r"\bFIXME\b", "FIXME marker"),
    (r"\bPLACEHOLDER\b", "PLACEHOLDER marker"),
    (r"<insert .+?>", "angle-bracket placeholder"),
    (r"<[A-Z][A-Z _]+>", "all-caps angle-bracket placeholder"),
]

FR_RE = re.compile(r"\*\*FR-\d{2,}\*\*\s*:", re.MULTILINE)
NFR_RE = re.compile(r"\*\*NFR-\d{2,}\*\*\s*:", re.MULTILINE)
US_RE = re.compile(
    r"(As an?)\s+.+?,\s+(I want to|I need to)\s+.+?,\s+(so that|in order to)\s+",
    re.IGNORECASE,
)
AC_CHECKBOX_RE = re.compile(r"- \[[ x]\]", re.IGNORECASE)
AC_GWT_RE = re.compile(r"\b(Given|When|Then)\b", re.IGNORECASE)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_spec(path: str) -> tuple[str, list[str]]:
    try:
        text = Path(path).read_text(encoding="utf-8")
        return text, text.splitlines()
    except FileNotFoundError:
        _fatal(f"File not found: {path}")
    except OSError as exc:
        _fatal(str(exc))


def _fatal(message: str) -> None:
    print(json.dumps({"error": message}), file=sys.stderr)
    sys.exit(2)


def extract_sections(lines: list[str]) -> dict[str, list[str]]:
    """Return a dict mapping H2 heading text → list of lines in that section."""
    sections: dict[str, list[str]] = {}
    current = "__preamble__"
    for line in lines:
        match = re.match(r"^##\s+(.+)$", line)
        if match:
            current = match.group(1).strip()
            sections[current] = []
        else:
            sections.setdefault(current, []).append(line)
    return sections


def section_text(sections: dict, keyword: str) -> str:
    """Return the joined text of the first section whose name contains keyword (case-insensitive)."""
    for name, body in sections.items():
        if keyword.lower() in name.lower():
            return "\n".join(body)
    return ""


def issue(severity: str, rule: str, message: str, line: int | None = None) -> dict:
    return {"severity": severity, "rule": rule, "message": message, "line": line}


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_title(lines: list[str]) -> list[dict]:
    for ln in lines[:10]:
        if re.match(r"^#\s+\S", ln):
            return []
    return [issue("error", "missing-title", "Spec must start with an H1 title (# Feature Name)")]


def check_required_sections(sections: dict) -> list[dict]:
    found = {k.lower() for k in sections}
    return [
        issue("error", "missing-section", f"Required section '## {s}' is missing")
        for s in REQUIRED_SECTIONS
        if s.lower() not in found
    ]


def check_no_code_blocks(lines: list[str]) -> list[dict]:
    problems = []
    in_block = False
    for i, ln in enumerate(lines, 1):
        if ln.strip().startswith("```"):
            if not in_block:
                in_block = True
                problems.append(
                    issue("error", "code-block-in-spec",
                          "Code blocks are not allowed — specs define WHAT, not HOW", line=i)
                )
            else:
                in_block = False
    return problems


def check_no_how_details(sections: dict) -> list[dict]:
    """Scan requirement and acceptance criteria sections for HOW-level details."""
    target = section_text(sections, "requirement") + "\n" + section_text(sections, "acceptance")
    problems = []
    for pattern, label in HOW_PATTERNS:
        if re.search(pattern, target, re.IGNORECASE):
            problems.append(
                issue("error", "implementation-detail",
                      f"Spec contains implementation detail ({label}) — move HOW details to plan.md")
            )
    return problems


def check_no_placeholders(lines: list[str]) -> list[dict]:
    compiled = [(re.compile(p, re.IGNORECASE), label) for p, label in PLACEHOLDER_PATTERNS]
    problems = []
    for i, ln in enumerate(lines, 1):
        for regex, label in compiled:
            if regex.search(ln):
                problems.append(
                    issue("error", "placeholder-text",
                          f"Line {i} contains unfilled placeholder ({label})", line=i)
                )
                break
    return problems


def check_requirements_numbered(sections: dict) -> list[dict]:
    req = section_text(sections, "requirement")
    problems = []
    if "functional" in req.lower() and not FR_RE.search(req):
        problems.append(
            issue("warning", "requirements-not-numbered",
                  "Functional requirements should use **FR-01**: numbering")
        )
    if "non-functional" in req.lower() and not NFR_RE.search(req):
        problems.append(
            issue("warning", "requirements-not-numbered",
                  "Non-functional requirements should use **NFR-01**: numbering")
        )
    return problems


def check_user_stories(sections: dict) -> list[dict]:
    us = section_text(sections, "user stor")
    if not us:
        return []
    if not US_RE.search(us):
        return [
            issue("warning", "user-story-format",
                  "User Stories should follow: As a <role>, I want to <action>, so that <benefit>")
        ]
    return []


def check_acceptance_criteria(sections: dict) -> list[dict]:
    ac = section_text(sections, "acceptance")
    if not ac:
        return []

    problems = []
    has_checkboxes = bool(AC_CHECKBOX_RE.search(ac))
    has_gwt = bool(AC_GWT_RE.search(ac))

    if not has_checkboxes and not has_gwt:
        problems.append(
            issue("warning", "acceptance-criteria-format",
                  "Acceptance Criteria should use - [ ] AC-01: Given … When … Then … format")
        )

    count = len(AC_CHECKBOX_RE.findall(ac))
    if count < 2:
        problems.append(
            issue("warning", "acceptance-criteria-count",
                  f"Only {count} acceptance criteria found; aim for at least 3 testable criteria")
        )
    return problems


def check_goals_content(sections: dict) -> list[dict]:
    problems = []
    for section_name in ("Goals", "Non-Goals"):
        body = section_text(sections, section_name)
        if not body:
            continue
        bullets = [ln for ln in body.splitlines() if ln.strip().startswith("-")]
        if not bullets:
            problems.append(
                issue("warning", "empty-section",
                      f"'## {section_name}' must contain at least one bullet item (- ...)")
            )
    return problems


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def validate(path: str) -> dict:
    content, lines = load_spec(path)
    sections = extract_sections(lines)

    problems: list[dict] = []
    problems += check_title(lines)
    problems += check_required_sections(sections)
    problems += check_no_code_blocks(lines)
    problems += check_no_how_details(sections)
    problems += check_no_placeholders(lines)
    problems += check_requirements_numbered(sections)
    problems += check_user_stories(sections)
    problems += check_acceptance_criteria(sections)
    problems += check_goals_content(sections)

    errors = sum(1 for p in problems if p["severity"] == "error")
    warnings = sum(1 for p in problems if p["severity"] == "warning")
    score = max(0, 100 - errors * 20 - warnings * 5)

    return {
        "valid": errors == 0,
        "score": score,
        "summary": {"errors": errors, "warnings": warnings, "file": path},
        "issues": problems,
    }


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python validate_spec.py <path-to-spec.md>", file=sys.stderr)
        sys.exit(2)

    result = validate(sys.argv[1])
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
