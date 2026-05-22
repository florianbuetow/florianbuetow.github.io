#!/usr/bin/env bash
set -euo pipefail

CONTENT_DIR="${1:-content}"

if ! command -v wtg2svg >/dev/null 2>&1; then
    printf "\033[0;31m  ✗ wtg2svg not found on PATH (run: just init)\033[0m\n"
    exit 1
fi

FOUND=0
RENDERED=0
ERRORS=0

while IFS= read -r -d '' wtg; do
    FOUND=$((FOUND + 1))
    svg="${wtg%.wtg2}.svg"
    if wtg2svg -static < "$wtg" > "$svg" 2>/tmp/wtg2svg-stderr.$$; then
        # Post-process: add border and replace gradient background with solid fill
        sed -i '' \
            -e 's|preserveAspectRatio="xMidYMid meet">|preserveAspectRatio="xMidYMid meet"><rect x="0" y="0" width="100%" height="100%" rx="10" ry="10" fill="#ffffff" stroke="#000000" stroke-width="2"/>|' \
            -e 's|style="fill:url(#wardleyGradient)"|fill="#ffffff"|' \
            -e 's|fill="rgb(250,250,252)" fill-opacity="1.0" stroke="rgb(200,200,210)" stroke-opacity="1.0"|fill="#f8f8f8" fill-opacity="1.0" stroke="#000000" stroke-opacity="1.0"|' \
            "$svg"
        RENDERED=$((RENDERED + 1))
        printf "  rendered: %s\n" "$svg"
    else
        ERRORS=$((ERRORS + 1))
        printf "\033[0;31m  ✗ failed: %s\033[0m\n" "$wtg"
        cat /tmp/wtg2svg-stderr.$$
    fi
done < <(find "$CONTENT_DIR" -type f -name '*.wtg2' -print0)

rm -f /tmp/wtg2svg-stderr.$$

if [ "$FOUND" -eq 0 ]; then
    printf "\033[0;32m  no .wtg2 files found in %s/\033[0m\n" "$CONTENT_DIR"
    exit 0
fi

if [ "$ERRORS" -gt 0 ]; then
    printf "\033[0;31m  ✗ %d/%d failed\033[0m\n" "$ERRORS" "$FOUND"
    exit 1
fi

printf "\033[0;32m  %d rendered, %d total\033[0m\n" "$RENDERED" "$FOUND"
