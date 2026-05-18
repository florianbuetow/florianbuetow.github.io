#!/usr/bin/env bash
# Guard: fail the build when any `draft: true` article still contains
# unresolved placeholder/TODO markers. By design this only scans drafts —
# the intent is to surface unfinished work before an article is flipped
# to `draft: false` and shipped.
set -euo pipefail

CONTENT_DIR="${1:-content}"
TMPFILE=$(mktemp)
trap 'rm -f "$TMPFILE"' EXIT

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
    # Only scan drafts (draft: true) — non-drafts are out of scope for this guard.
    if ! awk '/^---$/{n++} n==1{print} n==2{exit}' "$md" | grep -q '^draft: *true'; then
        continue
    fi

    for pat in "${patterns[@]}"; do
        if grep -nE -- "$pat" "$md" >> "$TMPFILE.raw" 2>/dev/null; then
            while IFS= read -r hit; do
                printf "%s:%s\n" "$md" "$hit" >> "$TMPFILE"
            done < "$TMPFILE.raw"
            : > "$TMPFILE.raw"
        fi
    done
done < <(find "$CONTENT_DIR" -name '*.md' -type f -print0)

ERRORS=$(wc -l < "$TMPFILE" | tr -d ' ')
if [ "$ERRORS" -gt 0 ]; then
    while IFS= read -r line; do
        printf "\033[0;31m  ✗ %s\033[0m\n" "$line"
    done < "$TMPFILE"
    printf "\033[0;31m✗ validate-content failed: %d placeholder marker(s) in draft articles\033[0m\n" "$ERRORS"
    exit 1
fi
printf "\033[0;32m  no unresolved placeholders found in draft articles\033[0m\n"
