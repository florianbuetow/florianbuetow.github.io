#!/usr/bin/env bash
set -euo pipefail

# Replaces em dashes (U+2014) in markdown files with ' - '.
#
# Usage:
#   ./fix-em-dashes.sh              # dry-run: show what would change, touch nothing
#   ./fix-em-dashes.sh --apply      # apply replacements
#   ./fix-em-dashes.sh --apply content/blog  # apply in a specific subtree
#
# Replacement rule:
#   ' — ' (space em-dash space) → ' - '  (keeps single space on each side)
#   '—'   (no surrounding spaces)        → '-'
#
# This is a safe default, not always the right substitute. Review the printed
# lines afterwards and fix cases where a period, comma, colon, or parentheses
# would read better. See docs/article-formatting.md §1.

APPLY=false
CONTENT_DIR="content"

for arg in "$@"; do
    case "$arg" in
        --apply) APPLY=true ;;
        --*) printf "\033[0;31m✗ Unknown flag: %s\033[0m\n" "$arg"; exit 1 ;;
        *) CONTENT_DIR="$arg" ;;
    esac
done

if [ ! -d "$CONTENT_DIR" ]; then
    printf "\033[0;31m✗ Directory not found: %s\033[0m\n" "$CONTENT_DIR"
    exit 1
fi

if [ "$APPLY" = false ]; then
    printf "\033[0;33mDry-run mode — no files will be modified. Pass --apply to write changes.\033[0m\n\n"
fi

FILES_CHANGED=0

while IFS= read -r -d '' file; do
    if ! grep -qF '—' "$file"; then
        continue
    fi

    printf "\033[0;34m%s\033[0m\n" "$file"
    grep -nF '—' "$file" | while IFS= read -r line; do
        printf "  %s\n" "$line"
    done
    printf "\n"

    if [ "$APPLY" = true ]; then
        sed -i '' 's/ — / - /g; s/—/-/g' "$file"
    fi

    FILES_CHANGED=$((FILES_CHANGED + 1))
done < <(find "$CONTENT_DIR" -name '*.md' -print0)

if [ "$FILES_CHANGED" -eq 0 ]; then
    printf "\033[0;32m✓ No em dashes found in %s\033[0m\n" "$CONTENT_DIR"
elif [ "$APPLY" = true ]; then
    printf "\033[0;33m⚠ Replaced em dashes in %d file(s). Review the lines above.\033[0m\n" "$FILES_CHANGED"
    printf "  Some replacements may need a period, comma, colon, or parens instead of ' - '.\n"
    printf "  See docs/article-formatting.md §1 for the substitution table.\n"
else
    printf "\033[0;33m%d file(s) have em dashes. Run with --apply to fix them.\033[0m\n" "$FILES_CHANGED"
fi
