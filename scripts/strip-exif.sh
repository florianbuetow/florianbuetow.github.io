#!/usr/bin/env bash
set -euo pipefail

CONTENT_DIR="${1:-content}"

OUTPUT=$(exiftool -all= -overwrite_original -r \
    -ext jpg -ext jpeg -ext png -ext gif -ext tiff -ext tif -ext webp \
    -ext mp4 -ext mov -ext avi -ext mkv \
    "$CONTENT_DIR" 2>&1)

UPDATED=$(echo "$OUTPUT" | grep "image files updated" | awk '{print $1}' || true)

if [ -n "$UPDATED" ] && [ "$UPDATED" -gt 0 ] 2>/dev/null; then
    printf "  %s file(s) stripped\n" "$UPDATED"
else
    printf "\033[0;32m  no metadata to strip in %s/\033[0m\n" "$CONTENT_DIR"
fi
