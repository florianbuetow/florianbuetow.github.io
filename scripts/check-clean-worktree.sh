#!/usr/bin/env bash
set -euo pipefail

if ! git diff --quiet || ! git diff --cached --quiet; then
    printf "\033[0;31m✗ check-clean-worktree failed: working tree is dirty\033[0m\n"
    git status --short | sed 's/^/    /'
    exit 1
fi
printf "\033[0;32m  working tree clean\033[0m\n"
