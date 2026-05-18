#!/usr/bin/env bash
# Tests for scripts/validate-content.sh
#
# Uses an isolated temp content tree so no real article is touched. Each case
# writes a synthetic markdown file with a specific (draft, TODO-marker) shape
# and asserts the script's exit code and hit count.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPT="$REPO_ROOT/scripts/validate-content.sh"

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

mk_article() {
    # $1 = path under $TMP, $2 = draft (true|false), $3 = body
    local p="$TMP/$1"
    mkdir -p "$(dirname "$p")"
    cat > "$p" <<EOF
---
title: "$1"
draft: $2
---

$3
EOF
}

# Run the script against $TMP. Captures exit code in $RC and hit count in $HITS.
# Hit count is parsed from the script's own summary line — robust against ANSI
# color codes in the output stream.
run_script() {
    local out
    set +e
    out="$(bash "$SCRIPT" "$TMP" 2>&1)"
    RC=$?
    set -e
    HITS="$(printf '%s\n' "$out" | sed -n 's/.*failed: \([0-9]*\) placeholder.*/\1/p' | head -1)"
    [ -z "$HITS" ] && HITS=0
    LAST="$out"
}

PASS=0
FAIL=0
assert() {
    # $1 = label, $2 = expected RC, $3 = expected hits, $4 = comparison op for hits ('eq' or 'ge')
    local label="$1" exp_rc="$2" exp_hits="$3" op="${4:-eq}"
    local ok=1
    [ "$RC" = "$exp_rc" ] || ok=0
    case "$op" in
        eq) [ "$HITS" = "$exp_hits" ] || ok=0 ;;
        ge) [ "$HITS" -ge "$exp_hits" ] || ok=0 ;;
    esac
    if [ "$ok" = 1 ]; then
        printf "\033[0;32m  ✓ %s (rc=%s hits=%s)\033[0m\n" "$label" "$RC" "$HITS"
        PASS=$((PASS+1))
    else
        printf "\033[0;31m  ✗ %s (rc=%s exp=%s, hits=%s exp%s%s)\033[0m\n" \
            "$label" "$RC" "$exp_rc" "$HITS" "$op" "$exp_hits"
        printf "%s\n" "$LAST" | sed 's/^/      /'
        FAIL=$((FAIL+1))
    fi
}

# ---------- T1: draft:true + TODO → fail with 1 hit ----------
rm -rf "${TMP:?}"/*; mk_article "t1/index.md" true "Body has a TODO marker."
run_script
assert "T1 draft:true with TODO blocks" 1 1

# ---------- T2: draft:true + clean content → pass ----------
rm -rf "${TMP:?}"/*; mk_article "t2/index.md" true "Clean body, no markers."
run_script
assert "T2 draft:true clean passes" 0 0

# ---------- T3: draft:false + TODO → script skips, pass ----------
rm -rf "${TMP:?}"/*; mk_article "t3/index.md" false "Body has a TODO marker."
run_script
assert "T3 draft:false with TODO is ignored" 0 0

# ---------- T4: draft:false + clean → pass ----------
rm -rf "${TMP:?}"/*; mk_article "t4/index.md" false "Clean body."
run_script
assert "T4 draft:false clean passes" 0 0

# ---------- T5: flip semantics — same file, toggled draft flag ----------
rm -rf "${TMP:?}"/*; mk_article "t5/index.md" true "[Comment on LinkedIn](LINK_TO_BE_ADDED)"
run_script
assert "T5a draft:true LINK_TO_BE_ADDED blocks" 1 1
# Flip to draft:false in place and re-run — must now pass.
sed -i.bak 's/^draft: true$/draft: false/' "$TMP/t5/index.md" && rm "$TMP/t5/index.md.bak"
run_script
assert "T5b same file flipped to draft:false passes" 0 0
# Flip back to draft:true — must block again.
sed -i.bak 's/^draft: false$/draft: true/' "$TMP/t5/index.md" && rm "$TMP/t5/index.md.bak"
run_script
assert "T5c same file flipped back to draft:true blocks" 1 1

# ---------- T6: each forbidden marker catches independently ----------
markers=(
    'TODO'
    'LINK_TO_BE_ADDED'
    'urn:li:activity:PLACEHOLDER'
    'placeholder.png'
    'file:///Users/local/path'
    'Image to commission: ring diagram'
)
i=0
for m in "${markers[@]}"; do
    i=$((i+1))
    rm -rf "${TMP:?}"/*; mk_article "t6_${i}/index.md" true "Marker line: $m"
    run_script
    assert "T6.$i marker '$m' detected" 1 1
done

# ---------- T7: mixed tree — only draft:true with markers counted ----------
rm -rf "${TMP:?}"/*
mk_article "a/index.md" true  "TODO here"
mk_article "b/index.md" false "TODO here (should be ignored)"
mk_article "c/index.md" true  "[link](LINK_TO_BE_ADDED)"
mk_article "d/index.md" true  "clean body"
run_script
assert "T7 mixed tree counts only draft:true hits" 1 2

# ---------- T8: word boundary on TODO ----------
# Bare "TODO" should match; "TODOSOMETHING" should not (boundary requirement).
rm -rf "${TMP:?}"/*; mk_article "t8a/index.md" true "ATTODOSOMETHING is fine"
run_script
assert "T8a TODOSOMETHING (no word boundary) does not match" 0 0
rm -rf "${TMP:?}"/*; mk_article "t8b/index.md" true "leading word TODO trailing"
run_script
assert "T8b bare TODO matches" 1 1

echo ""
if [ "$FAIL" -gt 0 ]; then
    printf "\033[0;31m✗ %d test(s) failed, %d passed\033[0m\n" "$FAIL" "$PASS"
    exit 1
fi
printf "\033[0;32m✓ all %d tests passed\033[0m\n" "$PASS"
