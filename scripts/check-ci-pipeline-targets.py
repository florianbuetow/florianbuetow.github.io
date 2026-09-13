#!/usr/bin/env python3
"""Fail if any Content-Checks or Tests target is not wired into ci and ci-verbose.

The justfile groups its targets in the `help` recipe under coloured headers
(e.g. `Content-Checks:`, `Tests:`). This check parses that help section to learn
which targets belong to those two groups, then parses the `ci` and `ci-verbose`
recipe bodies to see which targets they invoke via `just <target>`. Any group
target that a pipeline does not call is reported.

Exit code is 1 if any group target is missing from a pipeline, or if the help,
ci or ci-verbose recipe, or the Content-Checks or Tests group, cannot be found.
Otherwise the exit code is 0.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ANSI_RED = "\033[0;31m"
ANSI_GREEN = "\033[0;32m"
ANSI_RESET = "\033[0m"

# A coloured group header inside the help output, e.g. `\033[0;33mContent-Checks:\033[0m`.
GROUP_HEADER_RE = re.compile(r"\\033\[0;33m([A-Za-z][A-Za-z0-9-]*):\\033\[0m")
# A double-quoted string literal (help entries quote the target name and its description).
QUOTED_RE = re.compile(r'"([^"]*)"')
# A `just <target>` invocation inside a recipe body.
JUST_CALL_RE = re.compile(r"\bjust\s+([a-z][a-z0-9-]*)")


def fail(message: str) -> int:
    print(
        f"{ANSI_RED}✗ check-ci-pipeline-targets failed: {message}{ANSI_RESET}",
        file=sys.stderr,
    )
    return 1


def extract_recipe_body(lines: list[str], name: str) -> list[str] | None:
    """Return the body lines of recipe ``name``, or None if it is not defined.

    The header is matched anchored at column 0 and tolerates a parameter list
    before the colon (e.g. ``ci spelling='':``) and a dependency list after it
    (e.g. ``ci: build``), so the lookup keeps working if ``ci`` or ``ci-verbose``
    ever gain parameters or dependencies.
    """
    header_re = re.compile(rf"^{re.escape(name)}(\s[^:]*)?:")
    start = None
    for i, line in enumerate(lines):
        if header_re.match(line):
            start = i + 1
            break
    if start is None:
        return None
    body: list[str] = []
    for line in lines[start:]:
        if line.strip() == "":
            body.append(line)
            continue
        if line[0].isspace():
            body.append(line)
        else:
            break
    return body


def parse_help_groups(help_body: list[str]) -> dict[str, list[str]]:
    """Map each help group name to the ordered list of target names under it."""
    groups: dict[str, list[str]] = {}
    current: str | None = None
    for line in help_body:
        header = GROUP_HEADER_RE.search(line)
        if header:
            current = header.group(1)
            if current is not None:
                groups.setdefault(current, [])
            continue
        if current is None:
            continue
        quoted = QUOTED_RE.findall(line)
        # A help entry is `@printf "  %-36s %s\n" "<target>" "<description>"`:
        # the first quoted string is the printf format (it contains `%`), the
        # second is the target name.
        if len(quoted) >= 2 and "%" in quoted[0]:
            groups[current].append(quoted[1])
    return groups


def find_group(groups: dict[str, list[str]], name: str) -> list[str] | None:
    for key, targets in groups.items():
        if key.lower() == name.lower():
            return targets
    return None


def just_calls(body: list[str]) -> set[str]:
    return {target for line in body for target in JUST_CALL_RE.findall(line)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Fail if any Content-Checks or Tests target is not called by "
            "ci and ci-verbose."
        )
    )
    parser.add_argument(
        "--justfile",
        default="justfile",
        help="Path to the justfile to inspect (default: ./justfile).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    justfile = Path(args.justfile)
    try:
        lines = justfile.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        return fail(f"could not read {justfile}: {exc}")

    help_body = extract_recipe_body(lines, "help")
    if help_body is None:
        return fail(f"could not find the 'help' target in {justfile}")

    groups = parse_help_groups(help_body)
    content_checks = find_group(groups, "content-checks")
    if content_checks is None:
        return fail(f"could not find the 'Content-Checks:' group in {justfile}")
    tests = find_group(groups, "tests")
    if tests is None:
        return fail(f"could not find the 'Tests:' group in {justfile}")

    ci_body = extract_recipe_body(lines, "ci")
    if ci_body is None:
        return fail(f"could not find the 'ci' target in {justfile}")
    ci_verbose_body = extract_recipe_body(lines, "ci-verbose")
    if ci_verbose_body is None:
        return fail(f"could not find the 'ci-verbose' target in {justfile}")

    ci_calls = just_calls(ci_body)
    ci_verbose_calls = just_calls(ci_verbose_body)

    # Union of both groups, preserving help order, de-duplicated.
    expected: list[str] = []
    for target in content_checks + tests:
        if target not in expected:
            expected.append(target)

    missing_from_ci = [t for t in expected if t not in ci_calls]
    missing_from_ci_verbose = [t for t in expected if t not in ci_verbose_calls]

    if missing_from_ci or missing_from_ci_verbose:
        offenders = set(missing_from_ci) | set(missing_from_ci_verbose)
        print(
            f"{ANSI_RED}✗ check-ci-pipeline-targets failed: "
            f"{len(offenders)} target(s) not wired into the CI pipeline{ANSI_RESET}",
            file=sys.stderr,
        )
        if missing_from_ci:
            print(f"{ANSI_RED}Targets not called by 'ci':{ANSI_RESET}", file=sys.stderr)
            for target in missing_from_ci:
                print(f"{ANSI_RED}  - {target}{ANSI_RESET}", file=sys.stderr)
        if missing_from_ci_verbose:
            print(
                f"{ANSI_RED}Targets not called by 'ci-verbose':{ANSI_RESET}",
                file=sys.stderr,
            )
            for target in missing_from_ci_verbose:
                print(f"{ANSI_RED}  - {target}{ANSI_RESET}", file=sys.stderr)
        return 1

    print(
        f"{ANSI_GREEN}✓ all {len(expected)} Content-Checks and Tests targets "
        f"are called by ci and ci-verbose{ANSI_RESET}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
