#!/usr/bin/env bash
# Check code blocks in draft articles for lines exceeding MAX_LEN characters.
# Ignores mermaid and wardley map (wtg2) code blocks.
# Usage: check-code-line-length.sh [file]
#   No argument: checks all draft: true files under content/
#   With argument: checks that specific file
set -euo pipefail

MAX_LEN=76
TOTAL_ERRORS=0

TARGET="${1:-}"
if [ -n "$TARGET" ]; then
    DRAFTS="$TARGET"
else
    DRAFTS=$(grep -rl "^draft: true" content/ 2>/dev/null || true)
fi

if [ -z "$DRAFTS" ]; then
    printf "  no draft articles found\n"
    exit 0
fi

FENCE_OPEN='^(```|~~~)([a-zA-Z0-9_-]*)'
FENCE_CLOSE='^(```|~~~)'

while IFS= read -r mdfile; do
    [ -z "$mdfile" ] && continue
    file_errors=()
    in_block=0   # 0=outside, 1=inside checked block, 2=inside skipped block
    lineno=0

    while IFS= read -r line; do
        lineno=$((lineno + 1))

        if [ "$in_block" -eq 0 ]; then
            if [[ "$line" =~ $FENCE_OPEN ]]; then
                lang=$(echo "${BASH_REMATCH[2]}" | tr '[:upper:]' '[:lower:]')
                if [[ "$lang" == "mermaid" || "$lang" == "wardley" || "$lang" == "wtg2" ]]; then
                    in_block=2
                else
                    in_block=1
                fi
            fi
        elif [ "$in_block" -eq 1 ]; then
            if [[ "$line" =~ $FENCE_CLOSE ]]; then
                in_block=0
            else
                len=${#line}
                if [ "$len" -gt "$MAX_LEN" ]; then
                    truncated="${line:0:$MAX_LEN}"
                    file_errors+=("  Line $lineno: exceeds $MAX_LEN characters: \"$truncated\"...")
                fi
            fi
        else
            if [[ "$line" =~ $FENCE_CLOSE ]]; then
                in_block=0
            fi
        fi
    done < "$mdfile"

    if [ "${#file_errors[@]}" -gt 0 ]; then
        printf "\033[0;31m%s: contains the following violations:\033[0m\n" "$mdfile"
        for err in "${file_errors[@]}"; do
            printf "\033[0;31m%s\033[0m\n" "$err"
        done
        TOTAL_ERRORS=$((TOTAL_ERRORS + 1))
    else
        printf "\033[0;32m  ✓ no violations in: %s\033[0m\n" "$mdfile"
    fi
done <<< "$DRAFTS"

if [ "$TOTAL_ERRORS" -gt 0 ]; then
    printf "\033[0;31m✗ check-code-line-length: %d file(s) have code block lines exceeding %d characters\033[0m\n" "$TOTAL_ERRORS" "$MAX_LEN"
    exit 1
fi
