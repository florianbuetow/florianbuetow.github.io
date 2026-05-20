#!/usr/bin/env bash
# Guard: error when a published (draft: false) article contains placeholder markers;
# warn (no build failure) when a draft (draft: true) article contains them.
set -euo pipefail

CONTENT_DIR="${1:-content}"
ERRORS=$(mktemp)
WARNINGS=$(mktemp)
HITS=$(mktemp)
trap 'rm -f "$ERRORS" "$WARNINGS" "$HITS"' EXIT

# Forbidden markers (case-sensitive ERE patterns).
patterns=(
    '\bTODO\b'
    'LINK_TO_BE_ADDED'
    'urn:li:activity:PLACEHOLDER'
    'placeholder\.(png|gif|jpg|jpeg|webp)'
    'file:///'
    'Image to commission'
)

while IFS= read -r -d '' md; do
    if awk '/^---$/{n++} n==1{print} n==2{exit}' "$md" | grep -q '^draft: *true'; then
        is_draft=1
    else
        is_draft=0
    fi

    for pat in "${patterns[@]}"; do
        : > "$HITS"
        grep -nE -- "$pat" "$md" > "$HITS" 2>/dev/null || true
        if [ -s "$HITS" ]; then
            while IFS= read -r hit; do
                if [ "$is_draft" -eq 1 ]; then
                    printf "%s:%s\n" "$md" "$hit" >> "$WARNINGS"
                else
                    printf "%s:%s\n" "$md" "$hit" >> "$ERRORS"
                fi
            done < "$HITS"
        fi
    done
done < <(find "$CONTENT_DIR" -name '*.md' -type f -print0)

WARN_COUNT=$(wc -l < "$WARNINGS" | tr -d ' ')
if [ "$WARN_COUNT" -gt 0 ]; then
    while IFS= read -r line; do
        printf "\033[0;33m  ⚠ %s\033[0m\n" "$line"
    done < "$WARNINGS"
    printf "\033[0;33m⚠ validate-content: %d placeholder marker(s) in draft articles (warnings only)\033[0m\n" "$WARN_COUNT"
fi

ERROR_COUNT=$(wc -l < "$ERRORS" | tr -d ' ')
if [ "$ERROR_COUNT" -gt 0 ]; then
    while IFS= read -r line; do
        printf "\033[0;31m  ✗ %s\033[0m\n" "$line"
    done < "$ERRORS"
    printf "\033[0;31m✗ validate-content failed: %d placeholder marker(s) in published articles\033[0m\n" "$ERROR_COUNT"
    exit 1
fi

printf "\033[0;32m  no unresolved placeholders found in published articles\033[0m\n"
