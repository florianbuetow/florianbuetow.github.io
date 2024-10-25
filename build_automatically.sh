#!/bin/bash

# Define paths for temporary files
CURRENT_OUTPUT=$(mktemp /tmp/current_output.XXXXXX)
PREVIOUS_OUTPUT=$(mktemp /tmp/previous_output.XXXXXX)

# Remove previous temp file if it exists
[ -f "$PREVIOUS_OUTPUT" ] && rm "$PREVIOUS_OUTPUT"

# Detect if we are on macOS or Linux and set the stat format accordingly
if [[ "$OSTYPE" == "darwin"* ]]; then
  STAT_CMD="stat -f '%z' "  # macOS: %z (size in bytes)
else
  STAT_CMD="stat --format='%s' "  # Linux: %s (size in bytes)
fi

# Infinite loop to run every second
while true; do
  # Save file paths and sizes to the temporary current output file
  find . -type f \( -name "*.qmd" -o -name "*.yml" \) -exec sh -c "$STAT_CMD {} && echo {}" \; > "$CURRENT_OUTPUT"

  # Check if previous output exists (skip change detection if not)
  if [ -f "$PREVIOUS_OUTPUT" ]; then
    if ! diff -q "$CURRENT_OUTPUT" "$PREVIOUS_OUTPUT" > /dev/null; then
      ./build.sh
    fi
  fi

  # Update previous output for the next run
  mv "$CURRENT_OUTPUT" "$PREVIOUS_OUTPUT"

  # Sleep for 1 second
  sleep 1
done
