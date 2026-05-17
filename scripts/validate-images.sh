#!/usr/bin/env bash
set -euo pipefail

CONTENT_DIR="${1:-content}"
ERRORS=0
TMPFILE=$(mktemp)
trap 'rm -f "$TMPFILE"' EXIT

while IFS= read -r -d '' md; do
    # Skip draft posts
    if awk '/^---$/{n++} n==1{print} n==2{exit}' "$md" | grep -q '^draft: *true'; then
        continue
    fi

    dir="$(dirname "$md")"

    { grep -oE '!\[[^]]*\]\([^)]+\)' "$md" 2>/dev/null || true; } \
        | sed 's/^!\[[^]]*\](//' | sed 's/)$//' \
        | while IFS= read -r ref; do
            case "$ref" in
                http://*|https://*) continue ;;
            esac
            clean="${ref%%\?*}"
            clean="${clean%%#*}"
            clean="${clean%% \"*}"
            case "$clean" in
                /*) target="static$clean" ;;
                *)  target="$dir/$clean" ;;
            esac
            if [ ! -f "$target" ]; then
                printf "%s → %s\n" "$md" "$ref" >> "$TMPFILE"
            fi
        done
done < <(find "$CONTENT_DIR" -name '*.md' -type f -print0)

ERRORS=$(wc -l < "$TMPFILE" | tr -d ' ')
if [ "$ERRORS" -gt 0 ]; then
    while IFS= read -r line; do
        printf "\033[0;31m  ✗ broken: %s\033[0m\n" "$line"
    done < "$TMPFILE"
    printf "\033[0;31m✗ validate-images failed: %d broken reference(s)\033[0m\n" "$ERRORS"
    exit 1
fi
printf "\033[0;32m  all image references valid\033[0m\n"
