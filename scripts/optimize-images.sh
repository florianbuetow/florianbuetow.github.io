#!/usr/bin/env bash
set -euo pipefail

CONTENT_DIR="${1:-content}"
BACKUP_DIR="${2:-data/assets}"
MAX_SIDE=1440
QUALITY=99

FOUND=0
CONVERTED=0
SKIPPED=0

while IFS= read -r -d '' img; do
    FOUND=$((FOUND + 1))

    ext="${img##*.}"
    webp="${img%.*}.webp"

    if [ -f "$webp" ]; then
        SKIPPED=$((SKIPPED + 1))
        continue
    fi

    W=$(sips -g pixelWidth "$img" 2>/dev/null | awk '/pixelWidth/{print $2}')
    H=$(sips -g pixelHeight "$img" 2>/dev/null | awk '/pixelHeight/{print $2}')

    if [ -z "$W" ] || [ -z "$H" ]; then
        printf "\033[0;31m  ✗ cannot read dimensions: %s\033[0m\n" "$img"
        exit 1
    fi

    RESIZE=""
    MAX=$((W > H ? W : H))
    if [ "$MAX" -gt "$MAX_SIDE" ]; then
        if [ "$W" -ge "$H" ]; then
            RESIZE="-resize $MAX_SIDE 0"
        else
            RESIZE="-resize 0 $MAX_SIDE"
        fi
    fi

    # shellcheck disable=SC2086
    cwebp -q "$QUALITY" $RESIZE "$img" -o "$webp" >/dev/null 2>&1

    backup="$BACKUP_DIR/$img"
    mkdir -p "$(dirname "$backup")"
    mv "$img" "$backup"

    dir="$(dirname "$img")"
    base_orig="$(basename "$img")"
    base_webp="$(basename "$webp")"
    find "$dir" -maxdepth 1 -name '*.md' -exec sed -i '' "s|${base_orig}|${base_webp}|g" {} +

    CONVERTED=$((CONVERTED + 1))
    printf "  converted: %s (%dx%d)\n" "$img" "$W" "$H"
done < <(find "$CONTENT_DIR" -type f \( -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' \) -print0)

if [ "$FOUND" -eq 0 ]; then
    printf "\033[0;32m  no optimizable images found in %s/\033[0m\n" "$CONTENT_DIR"
else
    printf "\033[0;32m  %d converted, %d skipped, %d total\033[0m\n" "$CONVERTED" "$SKIPPED" "$FOUND"
fi
