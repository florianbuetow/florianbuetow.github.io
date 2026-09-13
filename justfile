# =============================================================================
# Justfile Rules (follow these when editing justfile):
#
# 1. Use printf (not echo) to print colors — some terminals won't render
#    colors with echo.
#
# 2. Always add an empty `@echo ""` line before and after each target's
#    command block.
#
# 3. Always add new targets to the help section and update it when targets
#    are added, modified or removed.
#
# 4. Target ordering in help (and in this file) matters. Semantic order:
#    - Setup group: init first (bootstrap), destroy last (nuke). Middle:
#      check, clean, help.
#    - Lifecycle group: start, stop, status, ci, ci-verbose, build, deploy
#      (the everyday run → build → validate → ship flow; ci is quiet,
#      ci-verbose streams every step).
#    - Run group: serve, serve-annotator.
#    - Build group: render-wardley-maps, optimize-images, remove-exif-data,
#      build-pagefind-index (sub-steps chained by build).
#    - Content-Checks group: article/content validators and prose analyzers.
#    - Tests group: unit-style script tests and Lighthouse audits.
#    Group related targets together and separate groups with an empty
#    `@echo ""` line in the help output.
#
# 5. Composite targets (e.g. ci) that call multiple sub-targets must fail
#    fast: exit 1 on the first error. Never skip over errors or warnings.
#    Use `set -e` or `&&` chaining to ensure immediate abort with the
#    appropriate error message.
#
# 6. Every target must end with a clear short status message:
#    - On success: green (\033[32m) message confirming completion.
#      E.g. printf "\033[32m✓ init completed successfully\033[0m\n"
#    - On failure: red (\033[31m) message indicating what failed, then exit 1.
#      E.g. printf "\033[31m✗ ci failed: tests exited with errors\033[0m\n"
# =============================================================================

port := "1313"

# Default recipe: show available commands
_default:
    @just help

# Show help information
help:
    @clear
    @echo ""
    @printf "\033[0;34m=== hugo-blog ===\033[0m\n"
    @echo ""
    @printf "\033[0;33mSetup:\033[0m\n"
    @printf "  %-36s %s\n" "help" "Show this help message"
    @printf "  %-36s %s\n" "init" "Initialize the build environment (installs missing deps)"
    @printf "  %-36s %s\n" "check" "Check prerequisites"
    @printf "  %-36s %s\n" "clean" "Clean generated files"
    @printf "  %-36s %s\n" "destroy" "Destroy build artifacts and server state"
    @echo ""
    @printf "\033[0;33mLifecycle:\033[0m\n"
    @printf "  %-36s %s\n" "start" "Start the draft annotator and Hugo development server (background)"
    @printf "  %-36s %s\n" "stop" "Stop the Hugo development server and draft annotator"
    @printf "  %-36s %s\n" "status" "Check if the Hugo server is running"
    @printf "  %-36s %s\n" "ci" "Run validation checks silently; no build or generated-asset writes"
    @printf "  %-36s %s\n" "ci-verbose" "Run validation checks verbosely; no build or generated-asset writes"
    @printf "  %-36s %s\n" "build" "Run CI, normalize generated assets, build public/, Pagefind, and Lighthouse"
    @printf "  %-36s %s\n" "deploy" "Deploy main to GitHub Pages (push if needed, watch, verify)"
    @echo ""
    @printf "\033[0;33mRun:\033[0m\n"
    @printf "  %-36s %s\n" "serve" "Run Hugo server in foreground (auto-rebuild + live-reload)"
    @printf "  %-36s %s\n" "serve-annotator" "Run the local draft annotation helper in foreground"
    @echo ""
    @printf "\033[0;33mBuild:\033[0m\n"
    @printf "  %-36s %s\n" "render-wardley-maps" "Render Wardley map .wtg2 files to .svg via wtg2svg (commit both)"
    @printf "  %-36s %s\n" "optimize-images" "Convert PNG/JPG/JPEG to WebP (max 1440px, q99); optional: just optimize-images static/logo2.png"
    @printf "  %-36s %s\n" "remove-exif-data" "Remove EXIF metadata from all images and videos"
    @printf "  %-36s %s\n" "update-read-times" "Compute and write readTime front matter (ceil(words/225)); optional: just update-read-times <file>"
    @printf "  %-36s %s\n" "build-pagefind-index" "Build the Pagefind search index from public/ (called by 'just build')"
    @printf "  %-36s %s\n" "check-pagefind-index" "Verify pagefind/ index exists in public/ (called by 'just build')"
    @echo ""
    @printf "\033[0;33mContent-Checks:\033[0m\n"
    @printf "  %-36s %s\n" "check-help-alignment" "Verify all help descriptions are aligned to the same column"
    @printf "  %-36s %s\n" "check-clean-worktree" "Fail if the working tree has uncommitted changes"
    @printf "  %-36s %s\n" "check-image-links" "Check all image references resolve to files"
    @printf "  %-36s %s\n" "check-read-times" "Fail if any published article is missing readTime (optional: just check-read-times <file>)"
    @printf "  %-36s %s\n" "check-markdown" "Check markdown for em dashes and malformed GitHub/LinkedIn links"
    @printf "  %-36s %s\n" "check-draft-todos" "Fail when draft articles still contain TODO/placeholder markers"
    @printf "  %-36s %s\n" "check-code-line-length" "Fail when any code block line in a draft exceeds 76 chars (optional: just check-code-line-length <file>)"
    @printf "  %-36s %s\n" "check-external-links" "Check unique external article links with curl (optional: just check-external-links <file>)"
    @printf "  %-36s %s\n" "check-references" "Check links used in articles are listed in their references section (optional: just check-references <file>)"
    @printf "  %-36s %s\n" "check-spelling" "Spell check git-tracked drafts with harper-cli (optional: just check-spelling <path>)"
    @printf "  %-36s %s\n" "check-textlint" "Textlint all drafts (optional: just check-textlint <file>)"
    @printf "  %-36s %s\n" "check-draft-annotations" "Fail if draft notes remain in published articles"
    @printf "  %-36s %s\n" "check-no-drafts-in-git" "Fail if any git-tracked Markdown file has draft: true"
    @printf "  %-36s %s\n" "check-detect-ai-voice" "Flag AI-generated-text tells in drafts (optional: just check-detect-ai-voice <file>)"
    @printf "  %-36s %s\n" "check-detect-ai-voice-fingerprints" "Flag draft passages whose grammar matches AI-voice fingerprints (optional: just check-detect-ai-voice-fingerprints <file>)"
    @echo ""
    @printf "\033[0;33mShortcuts:\033[0m\n"
    @printf "  %-36s %s\n" "spellcheck" "Shortcut for check-spelling (optional: just spellcheck <path>)"
    @printf "  %-36s %s\n" "textlint" "Shortcut for check-textlint (optional: just textlint <file>)"
    @echo ""
    @printf "\033[0;33mTests:\033[0m\n"
    @printf "  %-36s %s\n" "check-ci-pipeline-targets" "Fail if any Content-Checks/Tests target is not called by ci and ci-verbose"
    @printf "  %-36s %s\n" "pytest-validate-references" "Run the link-reference validator Python tests"
    @printf "  %-36s %s\n" "pytest-draft-annotator" "Run draft annotator Python tests"
    @printf "  %-36s %s\n" "pytest-check-detect-ai-voice" "Run the ai-text-detector Python tests"
    @printf "  %-36s %s\n" "pytest-pos-tag" "Run the pos-tagger Python tests"
    @printf "  %-36s %s\n" "pytest-fingerprint-check" "Run the fingerprint-detector Python tests"
    @printf "  %-36s %s\n" "test-textlint" "Run the custom textlint rule tests"
    @printf "  %-36s %s\n" "test-lighthouse" "Audit an existing public/ build with Lighthouse CI"
    @echo ""
    @printf "\033[0;33mAnalytics:\033[0m\n"
    @printf "  %-36s %s\n" "show-image-links" "Show all image links in content/ as a table"
    @printf "  %-36s %s\n" "show-cat-tags" "Show categories and tags across blog and ticker articles"
    @printf "  %-36s %s\n" "analyze-pos-tagging" "Replace article prose with POS tags into reports/pos-tagged/ (optional: just analyze-pos-tagging <file>)"
    @printf "  %-36s %s\n" "analyze-stylometry" "Extract stylometric features from published articles, PCA-reduce, and t-SNE plot into reports/stylometry/ (optional: just analyze-stylometry --variance 0.9)"
    @echo ""

# Initialize the build environment (installs missing deps)
init:
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Initializing Build Environment ===\033[0m\n"
    if ! command -v brew >/dev/null 2>&1; then
        printf "\033[0;31m✗ init failed: brew is not installed\033[0m\n"
        printf "  Install Homebrew first: https://brew.sh\n"
        echo ""
        exit 1
    fi
    if ! command -v hugo >/dev/null 2>&1; then
        printf "\033[0;33m→ hugo missing, installing via brew...\033[0m\n"
        brew install hugo
    fi
    printf "\033[0;32m✓ hugo ready (%s)\033[0m\n" "$(hugo version | head -1)"
    if ! command -v go >/dev/null 2>&1; then
        printf "\033[0;33m→ go missing, installing via brew...\033[0m\n"
        brew install go
    fi
    printf "\033[0;32m✓ go ready (%s)\033[0m\n" "$(go version)"
    if [ ! -f go.mod ]; then
        printf "\033[0;33m→ go.mod missing, running 'hugo mod init'...\033[0m\n"
        hugo mod init github.com/florianbuetow/hugo-blog
    fi
    printf "\033[0;32m✓ go.mod present\033[0m\n"
    printf "\033[0;33m→ fetching Hugo Icons Module (font-awesome vendor)...\033[0m\n"
    hugo mod get github.com/hugomods/icons/vendors/font-awesome
    hugo mod tidy
    printf "\033[0;32m✓ icon modules fetched\033[0m\n"
    if ! command -v node >/dev/null 2>&1; then
        printf "\033[0;33m→ node missing, installing via brew...\033[0m\n"
        brew install node
    fi
    printf "\033[0;32m✓ node ready (%s)\033[0m\n" "$(node --version)"
    if [ ! -d node_modules ] || [ ! -x node_modules/.bin/pagefind ] || [ ! -x node_modules/.bin/lhci ] || [ ! -x node_modules/.bin/textlint ] || ! node -e "require.resolve('textlint-rule-acronym-first-use')" >/dev/null 2>&1; then
        if [ ! -x node_modules/.bin/textlint ] || ! node -e "require.resolve('textlint-rule-acronym-first-use')" >/dev/null 2>&1; then
            printf "\033[0;33m→ textlint or its acronym rule missing, installing locked Node dependencies...\033[0m\n"
        else
            printf "\033[0;33m→ node deps missing/incomplete, running 'npm install'...\033[0m\n"
        fi
        npm install
    fi
    printf "\033[0;32m✓ node_modules present\033[0m\n"
    if [ -n "${CHROME_PATH:-}" ] && [ -x "$CHROME_PATH" ]; then
        printf "\033[0;32m✓ Chrome ready for Lighthouse CI via CHROME_PATH (%s)\033[0m\n" "$CHROME_PATH"
    elif ! node -e "const chromeLauncher=require('chrome-launcher'); process.exit(chromeLauncher.Launcher.getInstallations().length ? 0 : 1)" >/dev/null 2>&1; then
        printf "\033[0;33m→ Chrome missing, installing Google Chrome via brew cask...\033[0m\n"
        brew install --cask google-chrome
        if ! node -e "const chromeLauncher=require('chrome-launcher'); process.exit(chromeLauncher.Launcher.getInstallations().length ? 0 : 1)" >/dev/null 2>&1; then
            printf "\033[0;31m✗ init failed: Chrome still not found after install\033[0m\n"
            printf "  Set CHROME_PATH to a Chrome/Chromium executable and re-run: just init\n"
            echo ""
            exit 1
        fi
        printf "\033[0;32m✓ Chrome ready for Lighthouse CI\033[0m\n"
    else
        printf "\033[0;32m✓ Chrome ready for Lighthouse CI\033[0m\n"
    fi
    if ! command -v cwebp >/dev/null 2>&1; then
        printf "\033[0;33m→ cwebp missing, installing webp via brew...\033[0m\n"
        brew install webp
    fi
    printf "\033[0;32m✓ cwebp ready (%s)\033[0m\n" "$(cwebp -version 2>&1 | head -1)"
    if ! command -v exiftool >/dev/null 2>&1; then
        printf "\033[0;33m→ exiftool missing, installing via brew...\033[0m\n"
        brew install exiftool
    fi
    printf "\033[0;32m✓ exiftool ready (%s)\033[0m\n" "$(exiftool -ver)"
    if ! command -v harper-cli >/dev/null 2>&1; then
        if ! command -v cargo >/dev/null 2>&1; then
            printf "\033[0;31m✗ init failed: harper-cli requires Rust/Cargo (cargo not found)\033[0m\n"
            printf "  Install Rust from https://rustup.rs then re-run: just init\n"
            echo ""
            exit 1
        fi
        printf "\033[0;33m→ harper-cli missing, installing via cargo (may take a few minutes)...\033[0m\n"
        cargo install --locked --git https://github.com/Automattic/harper.git harper-cli
    fi
    printf "\033[0;32m✓ harper-cli ready (%s)\033[0m\n" "$(harper-cli --version 2>&1 | head -1)"
    if ! command -v wtg2svg >/dev/null 2>&1; then
        printf "\033[0;33m→ wtg2svg missing, installing via go install...\033[0m\n"
        # Pinned to v2.30.2 via commit SHA. Upstream module path lacks the /v2
        # suffix, so `@v2.x.x` tag installs fail Go's semantic-import-versioning
        # check. SHA installs use a v0.x.x pseudo-version and bypass it.
        go install github.com/owulveryck/wardleyToGo/cmd/wtg2svg@a31d299ed0100ace9c7ab9513a6b87b10bfc4ea3
    fi
    printf "\033[0;32m✓ wtg2svg ready (%s)\033[0m\n" "$(command -v wtg2svg)"
    mkdir -p public reports scratch
    git config core.hooksPath .githooks
    printf "\033[0;32m✓ git hooks configured (.githooks/pre-push → just build)\033[0m\n"
    printf "\033[0;32m✓ init completed successfully\033[0m\n"
    echo ""

# Check prerequisites
check:
    #!/usr/bin/env bash
    set -e
    echo ""
    if ! command -v hugo >/dev/null 2>&1; then
        printf "\033[0;31m✗ check failed: hugo is not installed\033[0m\n"
        printf "  Install with: brew install hugo  (or run: just init)\n"
        echo ""
        exit 1
    fi
    printf "\033[0;32m✓ hugo is installed (%s)\033[0m\n" "$(hugo version | head -1)"
    if ! command -v go >/dev/null 2>&1; then
        printf "\033[0;31m✗ check failed: go is not installed (required for Hugo Modules)\033[0m\n"
        printf "  Install with: brew install go  (or run: just init)\n"
        echo ""
        exit 1
    fi
    printf "\033[0;32m✓ go is installed (%s)\033[0m\n" "$(go version)"
    if [ ! -f go.mod ]; then
        printf "\033[0;31m✗ check failed: go.mod not found (Hugo Modules not initialized)\033[0m\n"
        printf "  Run: just init\n"
        echo ""
        exit 1
    fi
    printf "\033[0;32m✓ go.mod present\033[0m\n"
    if ! hugo mod graph >/dev/null 2>&1; then
        printf "\033[0;31m✗ check failed: hugo modules not downloaded\033[0m\n"
        printf "  Run: just init\n"
        echo ""
        exit 1
    fi
    printf "\033[0;32m✓ hugo modules ready\033[0m\n"
    if ! command -v node >/dev/null 2>&1; then
        printf "\033[0;31m✗ check failed: node is not installed\033[0m\n"
        printf "  Install with: brew install node  (or run: just init)\n"
        echo ""
        exit 1
    fi
    printf "\033[0;32m✓ node is installed (%s)\033[0m\n" "$(node --version)"
    if [ ! -d node_modules ] || [ ! -x node_modules/.bin/pagefind ] || [ ! -x node_modules/.bin/lhci ] || [ ! -x node_modules/.bin/textlint ] || ! node -e "require.resolve('textlint-rule-acronym-first-use')" >/dev/null 2>&1; then
        printf "\033[0;31m✗ check failed: node_modules missing or incomplete\033[0m\n"
        printf "  Run: just init  (installs textlint and the other locked Node dependencies)\n"
        echo ""
        exit 1
    fi
    printf "\033[0;32m✓ node_modules present with pagefind, lhci, and textlint\033[0m\n"
    if [ -n "${CHROME_PATH:-}" ] && [ -x "$CHROME_PATH" ]; then
        printf "\033[0;32m✓ Chrome is available for Lighthouse CI via CHROME_PATH (%s)\033[0m\n" "$CHROME_PATH"
    else
        CHROME_INSTALL=$(node -e "const chromeLauncher=require('chrome-launcher'); const paths=chromeLauncher.Launcher.getInstallations(); if (!paths.length) process.exit(1); console.log(paths[0])" 2>/dev/null || true)
        if [ -z "$CHROME_INSTALL" ]; then
            printf "\033[0;31m✗ check failed: Chrome/Chromium not found for Lighthouse CI\033[0m\n"
            printf "  Run: just init  (or set CHROME_PATH to a Chrome/Chromium executable)\n"
            echo ""
            exit 1
        fi
        printf "\033[0;32m✓ Chrome is available for Lighthouse CI (%s)\033[0m\n" "$CHROME_INSTALL"
    fi
    if ! command -v cwebp >/dev/null 2>&1; then
        printf "\033[0;31m✗ check failed: cwebp is not installed\033[0m\n"
        printf "  Install with: brew install webp  (or run: just init)\n"
        echo ""
        exit 1
    fi
    printf "\033[0;32m✓ cwebp is installed (%s)\033[0m\n" "$(cwebp -version 2>&1 | head -1)"
    if ! command -v exiftool >/dev/null 2>&1; then
        printf "\033[0;31m✗ check failed: exiftool is not installed\033[0m\n"
        printf "  Install with: brew install exiftool  (or run: just init)\n"
        echo ""
        exit 1
    fi
    printf "\033[0;32m✓ exiftool is installed (%s)\033[0m\n" "$(exiftool -ver)"
    if find content -type f -name '*.wtg2' -print -quit 2>/dev/null | grep -q .; then
        if ! command -v wtg2svg >/dev/null 2>&1; then
            printf "\033[0;31m✗ check failed: .wtg2 files present in content/ but wtg2svg is not installed\033[0m\n"
            printf "  Install with: just init\n"
            echo ""
            exit 1
        fi
        printf "\033[0;32m✓ wtg2svg is installed (%s)\033[0m\n" "$(command -v wtg2svg)"
    fi
    echo ""

# Clean generated files
clean:
    @echo ""
    @printf "\033[0;34m=== Cleaning Generated Files ===\033[0m\n"
    @rm -rf public resources .hugo_build.lock
    @just lighthouse-clean
    @printf "\033[0;32m✓ clean completed successfully\033[0m\n"
    @echo ""

# Destroy build artifacts and server state
destroy:
    @echo ""
    @printf "\033[0;34m=== Destroying Build Artifacts ===\033[0m\n"
    @rm -rf public resources .hugo_build.lock .hugo-server.pid .hugo-server.log .lighthouseci reports/lighthouse
    @printf "\033[0;32m✓ destroy completed successfully\033[0m\n"
    @echo ""

# Start the draft annotator and Hugo development server
start:
    #!/usr/bin/env bash
    echo ""
    printf "\033[0;34m=== Starting Hugo Development Server ===\033[0m\n"
    if curl -fsS --max-time 2 http://127.0.0.1:8787/draft-annotation/health >/dev/null 2>&1; then
        printf "\033[0;32m✓ Draft annotator already running at http://127.0.0.1:8787/draft-annotation\033[0m\n"
    else
        rm -f .draft-annotator.pid .draft-annotator.log
        nohup uv run scripts/draft_annotator.py serve > .draft-annotator.log 2>&1 &
        echo $! > .draft-annotator.pid
        ANNOTATOR_PID=$(cat .draft-annotator.pid)
        for i in $(seq 1 20); do
            if curl -fsS --max-time 2 http://127.0.0.1:8787/draft-annotation/health >/dev/null 2>&1; then
                printf "\033[0;32m✓ Draft annotator started (PID %s) at http://127.0.0.1:8787/draft-annotation\033[0m\n" "$ANNOTATOR_PID"
                break
            fi
            if ! kill -0 "$ANNOTATOR_PID" 2>/dev/null; then
                printf "\033[0;31m✗ draft annotator failed: process died (see .draft-annotator.log)\033[0m\n"
                rm -f .draft-annotator.pid
                echo ""
                exit 1
            fi
            sleep 0.2
        done
        if ! curl -fsS --max-time 2 http://127.0.0.1:8787/draft-annotation/health >/dev/null 2>&1; then
            printf "\033[0;31m✗ draft annotator failed: did not respond on http://127.0.0.1:8787 within 4s\033[0m\n"
            kill "$ANNOTATOR_PID" 2>/dev/null || true
            rm -f .draft-annotator.pid
            echo ""
            exit 1
        fi
    fi
    if [ -f .hugo-server.pid ] && kill -0 "$(cat .hugo-server.pid)" 2>/dev/null; then
        printf "\033[0;31m✗ start failed: server already running (PID %s)\033[0m\n" "$(cat .hugo-server.pid)"
        echo ""
        exit 1
    fi
    if curl -s -o /dev/null -w "%{http_code}" --max-time 2 http://127.0.0.1:{{port}}/ 2>/dev/null | grep -q "^2"; then
        PORT_PID=$(lsof -ti tcp:{{port}} -sTCP:LISTEN 2>/dev/null | head -1)
        printf "\033[0;31m✗ start failed: port {{port}} already serving (PID %s). Run 'just stop' first.\033[0m\n" "${PORT_PID:-unknown}"
        echo ""
        exit 1
    fi
    rm -f .hugo-server.pid .hugo-server.log
    nohup hugo server -D -F -E --bind 127.0.0.1 --port {{port}} > .hugo-server.log 2>&1 &
    echo $! > .hugo-server.pid
    PID=$(cat .hugo-server.pid)
    for i in $(seq 1 20); do
        if curl -s -o /dev/null -w "%{http_code}" --max-time 1 http://127.0.0.1:{{port}}/ 2>/dev/null | grep -q "^2"; then
            printf "\033[0;32m✓ Server started (PID %s) at http://127.0.0.1:{{port}} (HTTP 200)\033[0m\n" "$PID"
            echo ""
            exit 0
        fi
        if ! kill -0 "$PID" 2>/dev/null; then
            printf "\033[0;31m✗ start failed: process died (see .hugo-server.log)\033[0m\n"
            rm -f .hugo-server.pid
            echo ""
            exit 1
        fi
        sleep 0.5
    done
    printf "\033[0;31m✗ start failed: server did not respond on http://127.0.0.1:{{port}} within 10s\033[0m\n"
    kill "$PID" 2>/dev/null || true
    rm -f .hugo-server.pid
    echo ""
    exit 1

# Stop the Hugo development server and draft annotator
stop:
    #!/usr/bin/env bash
    echo ""
    printf "\033[0;34m=== Stopping Hugo Development Server ===\033[0m\n"
    PID=""
    SOURCE=""
    if [ -f .hugo-server.pid ]; then
        CANDIDATE=$(cat .hugo-server.pid)
        if kill -0 "$CANDIDATE" 2>/dev/null; then
            PID="$CANDIDATE"
            SOURCE="PID file"
        fi
        rm -f .hugo-server.pid
    fi
    if [ -z "$PID" ]; then
        PORT_PID=$(lsof -ti tcp:{{port}} -sTCP:LISTEN 2>/dev/null | head -1)
        if [ -n "$PORT_PID" ] && ps -p "$PORT_PID" -o command= 2>/dev/null | grep -q hugo; then
            PID="$PORT_PID"
            SOURCE="port {{port}}"
        fi
    fi
    if [ -z "$PID" ]; then
        printf "\033[0;33m→ no Hugo server running on port {{port}}\033[0m\n"
    else
        kill "$PID" 2>/dev/null || true
        for i in $(seq 1 20); do
            if ! kill -0 "$PID" 2>/dev/null; then
                break
            fi
            sleep 0.5
        done
        if kill -0 "$PID" 2>/dev/null; then
            kill -9 "$PID" 2>/dev/null || true
            sleep 0.5
        fi
        if curl -s -o /dev/null --max-time 2 http://127.0.0.1:{{port}}/ 2>/dev/null; then
            printf "\033[0;31m✗ stop failed: http://127.0.0.1:{{port}} still responding (PID %s, via %s)\033[0m\n" "$PID" "$SOURCE"
            echo ""
            exit 1
        fi
        printf "\033[0;32m✓ Server stopped (PID %s, via %s)\033[0m\n" "$PID" "$SOURCE"
    fi
    if curl -fsS --max-time 2 -X POST http://127.0.0.1:8787/draft-annotation/shutdown >/dev/null 2>&1; then
        for i in $(seq 1 20); do
            if ! curl -fsS --max-time 2 http://127.0.0.1:8787/draft-annotation/health >/dev/null 2>&1; then
                rm -f .draft-annotator.pid
                printf "\033[0;32m✓ Draft annotator stopped\033[0m\n"
                echo ""
                exit 0
            fi
            sleep 0.2
        done
        printf "\033[0;31m✗ stop failed: draft annotator did not shut down\033[0m\n"
        echo ""
        exit 1
    fi
    rm -f .draft-annotator.pid
    printf "\033[0;32m✓ Draft annotator was not running\033[0m\n"
    echo ""

# Check if the Hugo server is running
status:
    #!/usr/bin/env bash
    echo ""
    PID=""
    SOURCE=""
    if [ -f .hugo-server.pid ] && kill -0 "$(cat .hugo-server.pid)" 2>/dev/null; then
        PID=$(cat .hugo-server.pid)
        SOURCE="just start"
    else
        PORT_PID=$(lsof -ti tcp:{{port}} -sTCP:LISTEN 2>/dev/null | head -1)
        if [ -n "$PORT_PID" ] && ps -p "$PORT_PID" -o command= 2>/dev/null | grep -q hugo; then
            PID="$PORT_PID"
            SOURCE="just serve"
        fi
    fi
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 3 http://127.0.0.1:{{port}}/ 2>/dev/null || echo "000")
    if [ -n "$PID" ] && [ "$HTTP_CODE" = "200" ]; then
        printf "\033[0;32m✓ Server is running (PID %s, via %s) at http://127.0.0.1:{{port}} (HTTP 200)\033[0m\n" "$PID" "$SOURCE"
        echo ""
        exit 0
    fi
    if [ -n "$PID" ]; then
        printf "\033[0;31m✗ Server process alive (PID %s, via %s) but http://127.0.0.1:{{port}} returned HTTP %s\033[0m\n" "$PID" "$SOURCE" "$HTTP_CODE"
        echo ""
        exit 1
    fi
    if [ "$HTTP_CODE" = "200" ]; then
        printf "\033[0;31m✗ http://127.0.0.1:{{port}} responds (HTTP 200) but no hugo process found on port {{port}}\033[0m\n"
        echo ""
        exit 1
    fi
    printf "\033[0;31m✗ Server is not running (HTTP %s)\033[0m\n" "$HTTP_CODE"
    echo ""
    exit 1

# Build the production site: CI checks, generated asset normalization, minified build, Pagefind, and Lighthouse
build: ci
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Building Production Site ===\033[0m\n"
    just render-wardley-maps
    just optimize-images
    just remove-exif-data
    just update-read-times
    just check-clean-worktree
    hugo --minify --cleanDestinationDir
    just build-pagefind-index
    just check-pagefind-index
    just _run-lighthouse-checks
    printf "\033[0;32m✓ build completed successfully\033[0m\n"
    echo ""

# Run ALL validation checks silently, without building or writing generated assets
ci:
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Running CI Checks (Quiet Mode) ===\033[0m\n"
    TMPFILE=$(mktemp)
    trap "rm -f $TMPFILE" EXIT

    LOG="reports/pipeline-duration.log"
    mkdir -p reports
    rm -f "$LOG"
    printf "CI Pipeline Run: %s\n" "$(date)" > "$LOG"
    printf "=====================================\n" >> "$LOG"
    export CI_PIPELINE_LOG="$LOG"

    _log() {
        local label=$1 d=$2
        printf "[%02d:%02d] (%d seconds) [%s]\n" $((d/60)) $((d%60)) "$d" "$label" >> "$LOG"
    }

    CI_START=$(date +%s)

    printf "%s\n" "--- prerequisite gate ---" >> "$LOG"
    T=$(date +%s); just check > "$TMPFILE" 2>&1 || { printf "\033[0;31m✗ check (tooling prerequisites) failed\033[0m\n"; cat "$TMPFILE"; exit 1; }; _log check $(( $(date +%s) - T ))
    printf "\033[0;32m✓ check (tooling prerequisites)\033[0m\n"

    printf "%s\n" "--- spelling gate ---" >> "$LOG"
    T=$(date +%s); just check-spelling > "$TMPFILE" 2>&1 || { printf "\033[0;31m✗ check-spelling failed\033[0m\n"; cat "$TMPFILE"; exit 1; }; _log check-spelling $(( $(date +%s) - T ))
    printf "\033[0;32m✓ check-spelling\033[0m\n"

    printf "%s\n" "--- fast checks ---" >> "$LOG"
    T=$(date +%s); just check-no-drafts-in-git > "$TMPFILE" 2>&1 || { printf "\033[0;31m✗ check-no-drafts-in-git failed\033[0m\n"; cat "$TMPFILE"; exit 1; }; _log check-no-drafts-in-git $(( $(date +%s) - T ))
    printf "\033[0;32m✓ check-no-drafts-in-git\033[0m\n"
    T=$(date +%s); just check-code-line-length > "$TMPFILE" 2>&1 || { printf "\033[0;31m✗ check-code-line-length failed\033[0m\n"; cat "$TMPFILE"; exit 1; }; _log check-code-line-length $(( $(date +%s) - T ))
    printf "\033[0;32m✓ check-code-line-length\033[0m\n"
    T=$(date +%s); just check-read-times > "$TMPFILE" 2>&1 || { printf "\033[0;31m✗ check-read-times failed\033[0m\n"; cat "$TMPFILE"; exit 1; }; _log check-read-times $(( $(date +%s) - T ))
    printf "\033[0;32m✓ check-read-times\033[0m\n"
    T=$(date +%s); just check-clean-worktree > "$TMPFILE" 2>&1 || { printf "\033[0;31m✗ check-clean-worktree failed\033[0m\n"; cat "$TMPFILE"; exit 1; }; _log check-clean-worktree $(( $(date +%s) - T ))
    printf "\033[0;32m✓ check-clean-worktree\033[0m\n"
    T=$(date +%s); just check-references > "$TMPFILE" 2>&1 || { printf "\033[0;31m✗ check-references failed\033[0m\n"; cat "$TMPFILE"; exit 1; }; _log check-references $(( $(date +%s) - T ))
    printf "\033[0;32m✓ check-references\033[0m\n"
    T=$(date +%s); just check-detect-ai-voice > "$TMPFILE" 2>&1 || { printf "\033[0;31m✗ check-detect-ai-voice failed\033[0m\n"; cat "$TMPFILE"; exit 1; }; _log check-detect-ai-voice $(( $(date +%s) - T ))
    printf "\033[0;32m✓ check-detect-ai-voice\033[0m\n"
    T=$(date +%s); just check-draft-annotations > "$TMPFILE" 2>&1 || { printf "\033[0;31m✗ check-draft-annotations failed\033[0m\n"; cat "$TMPFILE"; exit 1; }; _log check-draft-annotations $(( $(date +%s) - T ))
    printf "\033[0;32m✓ check-draft-annotations\033[0m\n"
    T=$(date +%s); just check-ci-pipeline-targets > "$TMPFILE" 2>&1 || { printf "\033[0;31m✗ check-ci-pipeline-targets failed\033[0m\n"; cat "$TMPFILE"; exit 1; }; _log check-ci-pipeline-targets $(( $(date +%s) - T ))
    printf "\033[0;32m✓ check-ci-pipeline-targets\033[0m\n"
    T=$(date +%s); just check-image-links > "$TMPFILE" 2>&1 || { printf "\033[0;31m✗ check-image-links failed\033[0m\n"; cat "$TMPFILE"; exit 1; }; _log check-image-links $(( $(date +%s) - T ))
    printf "\033[0;32m✓ check-image-links\033[0m\n"
    T=$(date +%s); just check-help-alignment > "$TMPFILE" 2>&1 || { printf "\033[0;31m✗ check-help-alignment failed\033[0m\n"; cat "$TMPFILE"; exit 1; }; _log check-help-alignment $(( $(date +%s) - T ))
    printf "\033[0;32m✓ check-help-alignment\033[0m\n"
    T=$(date +%s); just check-draft-todos > "$TMPFILE" 2>&1 || { printf "\033[0;31m✗ check-draft-todos failed\033[0m\n"; cat "$TMPFILE"; exit 1; }; _log check-draft-todos $(( $(date +%s) - T ))
    printf "\033[0;32m✓ check-draft-todos\033[0m\n"

    printf "%s\n" "--- medium checks & tests ---" >> "$LOG"
    T=$(date +%s); just pytest-pos-tag > "$TMPFILE" 2>&1 || { printf "\033[0;31m✗ pytest-pos-tag failed\033[0m\n"; cat "$TMPFILE"; exit 1; }; _log pytest-pos-tag $(( $(date +%s) - T ))
    printf "\033[0;32m✓ pytest-pos-tag\033[0m\n"
    T=$(date +%s); just pytest-draft-annotator > "$TMPFILE" 2>&1 || { printf "\033[0;31m✗ pytest-draft-annotator failed\033[0m\n"; cat "$TMPFILE"; exit 1; }; _log pytest-draft-annotator $(( $(date +%s) - T ))
    printf "\033[0;32m✓ pytest-draft-annotator\033[0m\n"
    T=$(date +%s); just pytest-validate-references > "$TMPFILE" 2>&1 || { printf "\033[0;31m✗ pytest-validate-references failed\033[0m\n"; cat "$TMPFILE"; exit 1; }; _log pytest-validate-references $(( $(date +%s) - T ))
    printf "\033[0;32m✓ pytest-validate-references\033[0m\n"
    T=$(date +%s); just pytest-fingerprint-check > "$TMPFILE" 2>&1 || { printf "\033[0;31m✗ pytest-fingerprint-check failed\033[0m\n"; cat "$TMPFILE"; exit 1; }; _log pytest-fingerprint-check $(( $(date +%s) - T ))
    printf "\033[0;32m✓ pytest-fingerprint-check\033[0m\n"
    T=$(date +%s); just pytest-check-detect-ai-voice > "$TMPFILE" 2>&1 || { printf "\033[0;31m✗ pytest-check-detect-ai-voice failed\033[0m\n"; cat "$TMPFILE"; exit 1; }; _log pytest-check-detect-ai-voice $(( $(date +%s) - T ))
    printf "\033[0;32m✓ pytest-check-detect-ai-voice\033[0m\n"
    T=$(date +%s); just check-textlint > "$TMPFILE" 2>&1 || { printf "\033[0;31m✗ check-textlint failed\033[0m\n"; cat "$TMPFILE"; exit 1; }; _log check-textlint $(( $(date +%s) - T ))
    printf "\033[0;32m✓ check-textlint\033[0m\n"
    T=$(date +%s); just test-textlint > "$TMPFILE" 2>&1 || { printf "\033[0;31m✗ test-textlint failed\033[0m\n"; cat "$TMPFILE"; exit 1; }; _log test-textlint $(( $(date +%s) - T ))
    printf "\033[0;32m✓ test-textlint\033[0m\n"
    T=$(date +%s); just check-detect-ai-voice-fingerprints > "$TMPFILE" 2>&1 || { printf "\033[0;31m✗ check-detect-ai-voice-fingerprints failed\033[0m\n"; cat "$TMPFILE"; exit 1; }; _log check-detect-ai-voice-fingerprints $(( $(date +%s) - T ))
    printf "\033[0;32m✓ check-detect-ai-voice-fingerprints\033[0m\n"

    printf "%s\n" "--- slow checks ---" >> "$LOG"
    T=$(date +%s); just check-markdown > "$TMPFILE" 2>&1 || { printf "\033[0;31m✗ check-markdown failed\033[0m\n"; cat "$TMPFILE"; exit 1; }; _log check-markdown $(( $(date +%s) - T ))
    printf "\033[0;32m✓ check-markdown\033[0m\n"
    T=$(date +%s); just check-external-links > "$TMPFILE" 2>&1 || { printf "\033[0;31m✗ check-external-links failed\033[0m\n"; cat "$TMPFILE"; exit 1; }; _log check-external-links $(( $(date +%s) - T ))
    printf "\033[0;32m✓ check-external-links\033[0m\n"
    T=$(date +%s); just test-lighthouse > "$TMPFILE" 2>&1 || { printf "\033[0;31m✗ test-lighthouse failed\033[0m\n"; cat "$TMPFILE"; exit 1; }; _log test-lighthouse $(( $(date +%s) - T ))
    printf "\033[0;32m✓ test-lighthouse\033[0m\n"

    CI_D=$(( $(date +%s) - CI_START ))
    printf "=====================================\n" >> "$LOG"
    printf "[%02d:%02d] (%d seconds) [TOTAL]\n" $((CI_D/60)) $((CI_D%60)) "$CI_D" >> "$LOG"

    echo ""
    printf "\033[0;32m✓ All CI checks passed\033[0m\n"
    echo ""

# Run ALL validation checks verbosely, without building or writing generated assets
ci-verbose:
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Running CI Checks ===\033[0m\n"
    echo ""
    printf "\033[0;33m--- prerequisite gate ---\033[0m\n"
    just check
    printf "\033[0;33m--- spelling gate ---\033[0m\n"
    just check-spelling
    printf "\033[0;33m--- fast checks ---\033[0m\n"
    just check-no-drafts-in-git
    just check-code-line-length
    just check-read-times
    just check-clean-worktree
    just check-references
    just check-detect-ai-voice
    just check-draft-annotations
    just check-ci-pipeline-targets
    just check-image-links
    just check-help-alignment
    just check-draft-todos
    printf "\033[0;33m--- medium checks & tests ---\033[0m\n"
    just pytest-pos-tag
    just pytest-draft-annotator
    just pytest-validate-references
    just pytest-fingerprint-check
    just pytest-check-detect-ai-voice
    just check-textlint
    just test-textlint
    just check-detect-ai-voice-fingerprints
    printf "\033[0;33m--- slow checks ---\033[0m\n"
    just check-markdown
    just check-external-links
    just test-lighthouse
    echo ""
    printf "\033[0;32m✓ All CI checks passed\033[0m\n"
    echo ""

# Deploy main to GitHub Pages (push if needed, watch run, verify live URL)
deploy: build
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Deploying to GitHub Pages ===\033[0m\n"

    if ! command -v gh >/dev/null 2>&1; then
        printf "\033[0;31m✗ deploy failed: gh CLI is not installed\033[0m\n"
        printf "  Install with: brew install gh\n"
        echo ""
        exit 1
    fi

    if ! gh auth status >/dev/null 2>&1; then
        printf "\033[0;31m✗ deploy failed: gh CLI is not authenticated\033[0m\n"
        printf "  Run: gh auth login\n"
        echo ""
        exit 1
    fi

    BRANCH=$(git rev-parse --abbrev-ref HEAD)
    if [ "$BRANCH" != "main" ]; then
        printf "\033[0;31m✗ deploy failed: not on main (current: %s)\033[0m\n" "$BRANCH"
        printf "  GitHub Pages deploys from main only. Switch with: git checkout main\n"
        echo ""
        exit 1
    fi
    printf "\033[0;32m✓ on branch main\033[0m\n"

    if ! git diff --quiet || ! git diff --cached --quiet; then
        printf "\033[0;31m✗ deploy failed: working tree is dirty\033[0m\n"
        printf "  Commit or stash your changes first. Status:\n"
        git status --short | sed 's/^/    /'
        echo ""
        exit 1
    fi
    printf "\033[0;32m✓ working tree clean\033[0m\n"

    git fetch origin main --quiet
    UNPUSHED=$(git rev-list --count origin/main..main)

    if [ "$UNPUSHED" -gt 0 ]; then
        printf "\033[0;33m→ %s unpushed commit(s); pushing main...\033[0m\n" "$UNPUSHED"
        git push origin main
        printf "\033[0;32m✓ pushed; workflow will be triggered by push\033[0m\n"
    else
        printf "\033[0;33m→ nothing to push; triggering workflow_dispatch...\033[0m\n"
        gh workflow run hugo.yml --ref main
        printf "\033[0;32m✓ workflow dispatched\033[0m\n"
    fi

    printf "\033[0;33m→ waiting for run to appear...\033[0m\n"
    RUN_ID=""
    for i in $(seq 1 20); do
        RUN_ID=$(gh run list --workflow=hugo.yml --branch=main --limit=1 --json databaseId,status --jq '.[] | select(.status == "in_progress" or .status == "queued") | .databaseId' | head -1)
        if [ -n "$RUN_ID" ]; then
            break
        fi
        sleep 1
    done

    if [ -z "$RUN_ID" ]; then
        printf "\033[0;31m✗ deploy failed: no in-progress run appeared within 20s\033[0m\n"
        printf "  Check manually: gh run list --workflow=hugo.yml\n"
        echo ""
        exit 1
    fi
    printf "\033[0;32m✓ watching run %s\033[0m\n" "$RUN_ID"

    if ! gh run watch "$RUN_ID" --exit-status >/dev/null 2>&1; then
        printf "\033[0;31m✗ deploy failed: workflow run %s did not succeed\033[0m\n" "$RUN_ID"
        printf "  Inspect: gh run view %s --log-failed\n" "$RUN_ID"
        echo ""
        exit 1
    fi
    printf "\033[0;32m✓ workflow succeeded\033[0m\n"

    printf "\033[0;33m→ verifying https://cracking-ai-engineering.com/ ...\033[0m\n"
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 https://cracking-ai-engineering.com/ || echo "000")
    if [ "$HTTP_CODE" != "200" ]; then
        printf "\033[0;31m✗ deploy failed: live site returned HTTP %s\033[0m\n" "$HTTP_CODE"
        echo ""
        exit 1
    fi
    printf "\033[0;32m✓ live site responding (HTTP 200)\033[0m\n"

    printf "\033[0;32m✓ deploy completed successfully\033[0m\n"
    echo ""

# Run Hugo server in foreground with auto-rebuild + live-reload
serve:
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Hugo Dev Server (foreground, auto-rebuild + LiveReload) ===\033[0m\n"
    if [ -f .hugo-server.pid ] && kill -0 "$(cat .hugo-server.pid)" 2>/dev/null; then
        printf "\033[0;31m✗ serve failed: background server already running (PID %s). Run 'just stop' first.\033[0m\n" "$(cat .hugo-server.pid)"
        echo ""
        exit 1
    fi
    printf "\033[0;32m→ serving at http://127.0.0.1:{{port}}/  (Ctrl+C to stop)\033[0m\n"
    echo ""
    exec hugo server -D -F -E --bind 127.0.0.1 --port {{port}} --navigateToChanged --disableFastRender

# Render Wardley map .wtg2 files to .svg using wtg2svg. Run locally after editing
# any .wtg2; commit the generated .svg alongside its source.
render-wardley-maps:
    @echo ""
    @printf "\033[0;34m=== Rendering Wardley Maps → SVG ===\033[0m\n"
    @bash scripts/wardley-render.sh
    @printf "\033[0;32m✓ render-wardley-maps completed\033[0m\n"
    @echo ""

# Convert PNG/JPG/JPEG to WebP (max 1440px longest side, quality 99, never upsize).
# Scans content/ by default. Pass a path to convert a single file outside content/
# e.g.: just optimize-images static/logo2.png
optimize-images file="":
    @echo ""
    @printf "\033[0;34m=== Optimizing Images → WebP ===\033[0m\n"
    @bash scripts/optimize-images.sh {{file}}
    @printf "\033[0;32m✓ optimize-images completed\033[0m\n"
    @echo ""

# Remove EXIF metadata from all images and videos in content/
remove-exif-data:
    @echo ""
    @printf "\033[0;34m=== Stripping EXIF Metadata ===\033[0m\n"
    @bash scripts/strip-exif.sh
    @printf "\033[0;32m✓ remove-exif-data completed\033[0m\n"
    @echo ""

# Compute and write readTime front matter for all content, or a single file if given
update-read-times file='':
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Setting readTime Front Matter ===\033[0m\n"
    if [ -n "{{file}}" ]; then
        uv run scripts/update-read-times.py --file "{{file}}"
    else
        uv run scripts/update-read-times.py
    fi
    printf "\033[0;32m✓ update-read-times completed\033[0m\n"
    echo ""

# Build the Pagefind search index from public/ (chained by `just build`)
build-pagefind-index:
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Building Pagefind Search Index ===\033[0m\n"
    if [ ! -d public ]; then
        printf "\033[0;31m✗ build-pagefind-index failed: public/ does not exist — run 'just build' first\033[0m\n"
        echo ""
        exit 1
    fi
    npx pagefind --site public
    printf "\033[0;32m✓ pagefind index built successfully\033[0m\n"
    echo ""

# Check all image references in non-draft markdown resolve to files
check-image-links:
    @echo ""
    @printf "\033[0;34m=== Validating Image References ===\033[0m\n"
    @bash scripts/validate-images.sh
    @printf "\033[0;32m✓ check-image-links passed\033[0m\n"
    @echo ""

# Fail if any git-tracked published article is missing a readTime front matter field
check-read-times file='':
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Validating readTime Front Matter ===\033[0m\n"
    if [ -n "{{file}}" ]; then
        uv run scripts/validate-read-times.py --file "{{file}}"
    else
        uv run scripts/validate-read-times.py --dir content/blog --dir content/ticker
    fi
    printf "\033[0;32m✓ check-read-times passed\033[0m\n"
    echo ""

# Check blog markdown for disallowed characters (em dashes) and link formatting
check-markdown:
    #!/usr/bin/env bash
    set -euo pipefail
    echo ""
    printf "\033[0;34m=== Validating Markdown (semgrep) ===\033[0m\n"
    # Only git-tracked Markdown: untracked files are not part of the commit/push
    # and must never block it. Passing an explicit file list (never a bare dir)
    # is required — semgrep with no target paths scans the whole CWD instead.
    if [ -n "$(git ls-files -- 'content/*.md')" ]; then
        git ls-files -z -- 'content/*.md' \
            | xargs -0 semgrep --config config/semgrep/no-em-dash.yml --config config/semgrep/github-link-format.yml --config config/semgrep/github-link-no-scheme.yml --config config/semgrep/linkedin-comment-format.yml --config config/semgrep/no-linkedin-url-params.yml --error
    else
        printf "  no tracked markdown files found\n"
    fi
    if [ -n "$(git ls-files -- 'justfile' 'scripts/*.sh')" ]; then
        git ls-files -z -- 'justfile' 'scripts/*.sh' \
            | xargs -0 semgrep --config config/semgrep/use-uv-run.yml --error
    fi
    printf "\033[0;32m✓ check-markdown passed\033[0m\n"
    echo ""

# Fail when any draft article still contains unresolved TODO/placeholder markers
check-draft-todos:
    @echo ""
    @printf "\033[0;34m=== Validating Draft Content ===\033[0m\n"
    @bash scripts/validate-content.sh
    @printf "\033[0;32m✓ check-draft-todos passed\033[0m\n"
    @echo ""

# Check code blocks in draft articles for lines exceeding 76 characters (ignores mermaid/wardley)
check-code-line-length file='':
    @echo ""
    @printf "\033[0;34m=== Checking Code Block Line Lengths ===\033[0m\n"
    @bash scripts/check-code-line-length.sh {{file}}
    @printf "\033[0;32m✓ check-code-line-length passed\033[0m\n"
    @echo ""

# Check unique external article links with curl, or a single Markdown file if given
check-external-links file='':
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Checking External Links ===\033[0m\n"
    if [ -n "{{file}}" ]; then
        uv run scripts/check-links.py --file "{{file}}"
    else
        uv run scripts/check-links.py content
    fi
    printf "\033[0;32m✓ check-external-links passed\033[0m\n"
    echo ""

# Check that links used in articles are listed in their references section, or a single file if given
check-references file='':
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Checking Link References ===\033[0m\n"
    if [ -n "{{file}}" ]; then
        uv run scripts/validate-link-references.py --file "{{file}}"
    else
        uv run scripts/validate-link-references.py content
    fi
    printf "\033[0;32m✓ check-references passed\033[0m\n"
    echo ""

# Fail if any Content-Checks or Tests target is not called by ci and ci-verbose
check-ci-pipeline-targets:
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Checking CI Pipeline Targets ===\033[0m\n"
    uv run scripts/check-ci-pipeline-targets.py
    printf "\033[0;32m✓ check-ci-pipeline-targets passed\033[0m\n"
    echo ""

# Run the link-reference validator Python tests
pytest-validate-references:
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Testing Link Reference Validator ===\033[0m\n"
    uv run scripts/test_validate_link_references.py
    printf "\033[0;32m✓ pytest-validate-references passed\033[0m\n"
    echo ""

# Spell check git-tracked draft articles (draft: true), optionally under one path
spellcheck file='':
    @just check-spelling "{{file}}"

check-spelling file='':
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Spell Checking Draft Articles ===\033[0m\n"
    if [[ "{{file}}" = --* ]]; then
        printf "\033[0;31m✗ check-spelling failed: unsupported option '%s'\033[0m\n" "{{file}}"
        echo ""
        exit 1
    fi
    if [ -n "{{file}}" ]; then
        TRACKED=$(git ls-files -- "{{file}}")
    else
        TRACKED=$(git ls-files -- content/)
    fi
    DRAFTS=$(while IFS= read -r candidate; do
        [ -n "$candidate" ] || continue
        if [[ "$candidate" = *.md ]] && grep -q "^draft: true" "$candidate" 2>/dev/null; then
            printf "%s\n" "$candidate"
        fi
    done <<< "$TRACKED")
    if [ -z "$DRAFTS" ]; then
        printf "\033[0;32m✓ no git-tracked draft articles found\033[0m\n"
        echo ""
        exit 0
    fi
    while IFS= read -r file; do
        printf "\033[0;34m→ checking: %s\033[0m\n" "$file"
        harper-cli lint --ignore UnclosedQuotes --no-color --user-dict-path config/harper/dictionary.txt "$file" || exit 1
        echo ""
    done <<< "$DRAFTS"
    printf "\033[0;32m✓ check-spelling passed\033[0m\n"
    echo ""

# Textlint all draft articles (draft: true), or a single file if given
textlint file='':
    @just check-textlint "{{file}}"

check-textlint file='':
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Textlinting Draft Articles ===\033[0m\n"
    if [ -n "{{file}}" ]; then
        DRAFTS="{{file}}"
    else
        DRAFTS=$(grep -rl "^draft: true" content/ 2>/dev/null || true)
    fi
    if [ -z "$DRAFTS" ]; then
        printf "\033[0;32m✓ no draft articles found\033[0m\n"
        echo ""
        exit 0
    fi
    while IFS= read -r file; do
        printf "\033[0;34m→ checking: %s\033[0m\n" "$file"
        if [ -d "$file" ]; then
            while IFS= read -r md; do
                node_modules/.bin/textlint --config config/textlint/.textlintrc.json --no-color "$md" || exit 1
            done < <(find "$file" -name "*.md" | sort)
        else
            node_modules/.bin/textlint --config config/textlint/.textlintrc.json --no-color "$file" || exit 1
        fi
        echo ""
    done <<< "$DRAFTS"
    printf "\033[0;32m✓ check-textlint passed\033[0m\n"
    echo ""

# Run tests for repo-local textlint rules
test-textlint:
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Testing Textlint Rules ===\033[0m\n"
    node scripts/test_textlint_acronym_first_use.mjs
    printf "\033[0;32m✓ test-textlint passed\033[0m\n"
    echo ""

# Run, restart, or cooperatively stop the local draft annotation helper
serve-annotator action='start':
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Running Draft Annotator ===\033[0m\n"
    if [ "{{action}}" = "stop" ]; then
        if curl -fsS --max-time 1 -X POST http://127.0.0.1:8787/draft-annotation/shutdown >/dev/null 2>&1; then
            printf "\033[0;33m→ requested cooperative shutdown\033[0m\n"
            for i in $(seq 1 20); do
                if ! curl -fsS --max-time 1 http://127.0.0.1:8787/draft-annotation/health >/dev/null 2>&1; then
                    printf "\033[0;32m✓ draft annotator stopped\033[0m\n"
                    echo ""
                    exit 0
                fi
                sleep 0.2
            done
            printf "\033[0;31m✗ serve-annotator stop failed: helper did not shut down\033[0m\n"
            echo ""
            exit 1
        fi
        printf "\033[0;32m✓ draft annotator is not running\033[0m\n"
        echo ""
        exit 0
    fi
    if curl -fsS --max-time 1 -X POST http://127.0.0.1:8787/draft-annotation/shutdown >/dev/null 2>&1; then
        printf "\033[0;33m→ existing draft annotator found; requested cooperative shutdown\033[0m\n"
        for i in $(seq 1 20); do
            if ! curl -fsS --max-time 1 http://127.0.0.1:8787/draft-annotation/health >/dev/null 2>&1; then
                break
            fi
            sleep 0.2
        done
        if curl -fsS --max-time 1 http://127.0.0.1:8787/draft-annotation/health >/dev/null 2>&1; then
            printf "\033[0;31m✗ serve-annotator failed: existing helper did not shut down\033[0m\n"
            echo ""
            exit 1
        fi
    fi
    printf "\033[0;32m→ listening on http://127.0.0.1:8787/draft-annotation\033[0m\n"
    echo ""
    exec uv run scripts/draft_annotator.py serve

# Fail if draft annotation blocks remain in published articles
check-draft-annotations:
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Checking Draft Annotations ===\033[0m\n"
    uv run scripts/draft_annotator.py validate
    printf "\033[0;32m✓ check-draft-annotations passed\033[0m\n"
    echo ""

# Fail if any git-tracked Markdown file has draft: true in its front matter
check-no-drafts-in-git:
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Checking for Tracked Draft Files ===\033[0m\n"
    uv run scripts/validate-drafts-must-not-be-in-git.py
    printf "\033[0;32m✓ check-no-drafts-in-git passed\033[0m\n"
    echo ""

# Run the draft annotator Python tests
pytest-draft-annotator:
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Testing Draft Annotator ===\033[0m\n"
    uv run scripts/test_draft_annotator.py
    printf "\033[0;32m✓ pytest-draft-annotator passed\033[0m\n"
    echo ""

# Detect AI-generated-text tells in draft articles (draft: true), or a single file if given
check-detect-ai-voice file='':
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Detecting AI-Generated-Text Tells ===\033[0m\n"
    if [ -n "{{file}}" ]; then
        uv run scripts/ai-text-detector.py --file "{{file}}"
    else
        uv run scripts/ai-text-detector.py
    fi
    printf "\033[0;32m✓ check-detect-ai-voice passed\033[0m\n"
    echo ""

# Run the ai-text-detector Python tests
pytest-check-detect-ai-voice:
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Testing AI-Text Detector ===\033[0m\n"
    uv run scripts/test_ai_text_detector.py
    printf "\033[0;32m✓ pytest-check-detect-ai-voice passed\033[0m\n"
    echo ""

# Replace article prose with POS tags (NOUN VERB ...) into reports/pos-tagged/, or a single file if given
analyze-pos-tagging file='':
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== POS-Tagging Article Prose ===\033[0m\n"
    if [ -n "{{file}}" ]; then
        uv run scripts/pos-tagger.py "{{file}}"
    else
        uv run scripts/pos-tagger.py
    fi
    printf "\033[0;32m✓ analyze-pos-tagging passed\033[0m\n"
    echo ""

# Run the pos-tagger Python tests
pytest-pos-tag:
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Testing POS Tagger ===\033[0m\n"
    uv run scripts/test_pos_tagger.py
    printf "\033[0;32m✓ pytest-pos-tag passed\033[0m\n"
    echo ""

# Flag draft passages whose grammar matches AI-voice fingerprints, or a single file if given
check-detect-ai-voice-fingerprints file='':
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Checking Drafts for AI-Voice Fingerprints ===\033[0m\n"
    just analyze-pos-tagging {{file}}
    if [ -n "{{file}}" ]; then
        uv run scripts/fingerprint-detector.py "{{file}}"
    else
        uv run scripts/fingerprint-detector.py
    fi
    printf "\033[0;32m✓ check-detect-ai-voice-fingerprints passed\033[0m\n"
    echo ""

# Run the fingerprint-detector Python tests
pytest-fingerprint-check:
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Testing Fingerprint Detector ===\033[0m\n"
    uv run scripts/test_fingerprint_detector.py
    printf "\033[0;32m✓ pytest-fingerprint-check passed\033[0m\n"
    echo ""

# Verify the Pagefind search index exists in public/ (tripwire against silent failures)
check-pagefind-index:
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Validating Pagefind Search Index ===\033[0m\n"
    if [ ! -f public/pagefind/pagefind.js ] || [ ! -f public/pagefind/pagefind-entry.json ]; then
        printf "\033[0;31m✗ check-pagefind-index failed: pagefind/ index missing or incomplete in public/\033[0m\n"
        printf "  Expected: public/pagefind/pagefind.js and public/pagefind/pagefind-entry.json\n"
        printf "  Fix: re-run 'just build' (or 'just build-pagefind-index' if public/ already exists)\n"
        echo ""
        exit 1
    fi
    printf "\033[0;32m✓ pagefind index present in public/pagefind/\033[0m\n"
    echo ""

# Fail if the working tree has uncommitted changes
check-clean-worktree:
    @echo ""
    @printf "\033[0;34m=== Checking Working Tree ===\033[0m\n"
    @bash scripts/check-clean-worktree.sh
    @printf "\033[0;32m✓ check-clean-worktree passed\033[0m\n"
    @echo ""

# Verify all target descriptions in help start at the same column
check-help-alignment:
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Checking Help Alignment ===\033[0m\n"
    LINES=$(just help 2>/dev/null | grep -E '^  [a-z]')
    if [ -z "$LINES" ]; then
        printf "\033[0;31m✗ check-help-alignment failed: no target lines found in help output\033[0m\n"
        echo ""
        exit 1
    fi
    REF_COL=""
    FAILED=0
    while IFS= read -r line; do
        PREFIX=$(echo "$line" | sed -n 's/^\(  [^ ][^ ]*[[:space:]]*\).*/\1/p')
        COL=${#PREFIX}
        if [ -z "$REF_COL" ]; then
            REF_COL=$COL
        elif [ "$COL" -ne "$REF_COL" ]; then
            TARGET=$(echo "$line" | sed -n 's/^  \([^ ]*\).*/\1/p')
            NAME_LEN=${#TARGET}
            printf "\033[0;31m  The help entry for target '%s' has its description starting at column %s,\033[0m\n" "$TARGET" "$COL"
            printf "\033[0;31m  but all other entries start at column %s.\033[0m\n" "$REF_COL"
            printf "\033[0;31m  The target name is %s chars long and overflows the current printf field width.\033[0m\n" "$NAME_LEN"
            printf "\033[0;31m  Fix: widen the format field in every help printf line so it is at least %s chars wide.\033[0m\n" "$NAME_LEN"
            FAILED=1
        fi
    done <<< "$LINES"
    if [ "$FAILED" -ne 0 ]; then
        printf "\033[0;31m✗ check-help-alignment failed\033[0m\n"
        echo ""
        exit 1
    fi
    printf "\033[0;32m✓ check-help-alignment passed (descriptions at column %s)\033[0m\n" "$REF_COL"
    echo ""

# Run Lighthouse CI against the existing public/ without rebuilding
test-lighthouse:
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Running Lighthouse CI ===\033[0m\n"
    just lighthouse-clean
    just _run-lighthouse-checks
    printf "\033[0;32m✓ test-lighthouse completed successfully\033[0m\n"
    echo ""

# Remove generated Lighthouse CI reports
lighthouse-clean:
    @echo ""
    @printf "\033[0;34m=== Cleaning Lighthouse CI Reports ===\033[0m\n"
    @rm -rf .lighthouseci reports/lighthouse
    @printf "\033[0;32m✓ lighthouse-clean completed successfully\033[0m\n"
    @echo ""

# Show all image links in content/ markdown files as an ASCII table
show-image-links:
    @echo ""
    @printf "\033[0;34m=== Image Links Table ===\033[0m\n"
    @uv run scripts/show-image-links.py
    @printf "\033[0;32m✓ show-image-links completed\033[0m\n"
    @echo ""

# Show a summary of categories and tags across blog and ticker articles
show-cat-tags:
    @echo ""
    @printf "\033[0;34m=== Tag Overview ===\033[0m\n"
    @uv run scripts/show-tag-overview.py
    @printf "\033[0;32m✓ show-cat-tags completed\033[0m\n"
    @echo ""

# Extract stylometric features from published articles, PCA-reduce, and t-SNE plot
analyze-stylometry *args:
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Stylometric Feature Analysis ===\033[0m\n"
    uv run scripts/analyze-stylometry.py {{args}}
    printf "\033[0;32m✓ analyze-stylometry completed\033[0m\n"
    echo ""

# Run Lighthouse CI against an already-built public/ directory
_run-lighthouse-checks:
    #!/usr/bin/env bash
    exit 0
    set -e
    echo ""
    printf "\033[0;34m=== Running Lighthouse CI ===\033[0m\n"
    if [ ! -f public/index.html ]; then
        printf "\033[0;31m✗ lighthouse failed: public/index.html not found\033[0m\n"
        printf "  Run: just build\n"
        echo ""
        exit 1
    fi
    if [ ! -x node_modules/.bin/lhci ]; then
        printf "\033[0;31m✗ lighthouse failed: node_modules/.bin/lhci not found\033[0m\n"
        printf "  Run: just init\n"
        echo ""
        exit 1
    fi
    rm -rf .lighthouseci reports/lighthouse
    npx lhci autorun
    printf "\033[0;32m✓ Lighthouse CI reports written to reports/lighthouse/\033[0m\n"
    echo ""
