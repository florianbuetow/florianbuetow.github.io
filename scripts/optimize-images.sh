#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="data/assets"
MAX_SIDE=1440
QUALITY=99

FOUND=0
CONVERTED=0
SKIPPED=0

convert_image() {
    local img="$1"
    FOUND=$((FOUND + 1))

    local webp="${img%.*}.webp"
    if [ -f "$webp" ]; then
        SKIPPED=$((SKIPPED + 1))
        return
    fi

    local W H
    W=$(sips -g pixelWidth "$img" 2>/dev/null | awk '/pixelWidth/{print $2}')
    H=$(sips -g pixelHeight "$img" 2>/dev/null | awk '/pixelHeight/{print $2}')

    if [ -z "$W" ] || [ -z "$H" ]; then
        printf "\033[0;31m  ✗ cannot read dimensions: %s\033[0m\n" "$img"
        exit 1
    fi

    local RESIZE=""
    local MAX=$((W > H ? W : H))
    if [ "$MAX" -gt "$MAX_SIDE" ]; then
        if [ "$W" -ge "$H" ]; then
            RESIZE="-resize $MAX_SIDE 0"
        else
            RESIZE="-resize 0 $MAX_SIDE"
        fi
    fi

    # shellcheck disable=SC2086
    cwebp -q "$QUALITY" $RESIZE "$img" -o "$webp" >/dev/null 2>&1

    local backup="$BACKUP_DIR/$img"
    mkdir -p "$(dirname "$backup")"
    mv "$img" "$backup"

    local dir base_orig base_webp
    dir="$(dirname "$img")"
    base_orig="$(basename "$img")"
    base_webp="$(basename "$webp")"
    find "$dir" -maxdepth 1 -name '*.md' -exec sed -i '' "s|${base_orig}|${base_webp}|g" {} +

    CONVERTED=$((CONVERTED + 1))
    printf "  converted: %s (%dx%d)\n" "$img" "$W" "$H"
}

ARG="${1:-}"

if [ -n "$ARG" ] && [ -f "$ARG" ]; then
    # Single-file mode: convert the given file directly
    convert_image "$ARG"
else
    # Directory mode: scan content/ (or the provided directory)
    CONTENT_DIR="${ARG:-content}"
    while IFS= read -r -d '' img; do
        convert_image "$img"
    done < <(find "$CONTENT_DIR" -type f \( -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' \) -print0)
fi

if [ "$FOUND" -eq 0 ]; then
    printf "\033[0;32m  no optimizable images found\033[0m\n"
else
    printf "\033[0;32m  %d converted, %d skipped, %d total\033[0m\n" "$CONVERTED" "$SKIPPED" "$FOUND"
fi
