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
#    - Run group: start, stop, status, dev.
#    - Building group: ci, build.
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
    @printf "  %-18s %s\n" "help" "Show this help message"
    @printf "  %-18s %s\n" "init" "Initialize the build environment (installs missing deps)"
    @printf "  %-18s %s\n" "check" "Check prerequisites"
    @printf "  %-18s %s\n" "clean" "Clean generated files"
    @printf "  %-18s %s\n" "destroy" "Destroy build artifacts and server state"
    @echo ""
    @printf "\033[0;33mRun:\033[0m\n"
    @printf "  %-18s %s\n" "start" "Start the Hugo development server (background)"
    @printf "  %-18s %s\n" "stop" "Stop the Hugo development server"
    @printf "  %-18s %s\n" "status" "Check if the Hugo server is running"
    @printf "  %-18s %s\n" "dev" "Run Hugo server in foreground (auto-rebuild + live-reload)"
    @echo ""
    @printf "\033[0;33mBuilding:\033[0m\n"
    @printf "  %-18s %s\n" "ci" "Run ALL validation checks (verbose)"
    @printf "  %-18s %s\n" "ci-quiet" "Run ALL validation checks silently (only show output on errors)"
    @printf "  %-18s %s\n" "strip-exif" "Remove EXIF metadata from all images and videos"
    @printf "  %-18s %s\n" "optimize-images" "Convert PNG/JPG/JPEG to WebP (max 1440px, q99); optional: just optimize-images static/logo2.png"
    @printf "  %-18s %s\n" "wardley-render" "Render Wardley map .wtg2 files to .svg via wtg2svg (commit both)"
    @printf "  %-18s %s\n" "validate-images" "Check all image references resolve to files"
    @printf "  %-18s %s\n" "check-links" "Check unique external article links with curl (optional: just check-links <file>)"
    @printf "  %-18s %s\n" "validate-md" "Check blog markdown for disallowed characters (em dashes)"
    @printf "  %-18s %s\n" "validate-content" "Fail when draft articles still contain TODO/placeholder markers"
    @printf "  %-18s %s\n" "check-code-line-length" "Fail when any code block line in a draft exceeds 76 chars (optional: just check-code-line-length <file>)"
    @printf "  %-18s %s\n" "spell-check" "Spell check all drafts with harper-cli (optional: just spell-check <file>)"
    @printf "  %-18s %s\n" "build" "Build the production site (optimize → validate → hugo → pagefind)"
    @printf "  %-18s %s\n" "build-pagefind-index" "Build the Pagefind search index from public/ (called by 'just build')"
    @printf "  %-18s %s\n" "validate-pagefind-index" "Verify pagefind/ index exists in public/ (tripwire against silent failures)"
    @printf "  %-18s %s\n" "check-clean-worktree" "Fail if the working tree has uncommitted changes"
    @printf "  %-18s %s\n" "check-clean-worktree" "Fail if the working tree has uncommitted changes"
    @printf "  %-18s %s\n" "run-lighthouse-checks" "Build and audit public/ with Lighthouse CI on a temporary local server"
    @printf "  %-18s %s\n" "lighthouse-clean" "Remove generated Lighthouse CI reports"
    @printf "  %-18s %s\n" "lighthouse-open" "Open representative Lighthouse HTML reports"
    @printf "  %-18s %s\n" "deploy" "Deploy main to GitHub Pages (push if needed, watch, verify)"
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
    if [ ! -d node_modules ] || [ ! -x node_modules/.bin/pagefind ] || [ ! -x node_modules/.bin/lhci ]; then
        printf "\033[0;33m→ node deps missing/incomplete, running 'npm install'...\033[0m\n"
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
    mkdir -p public
    git config core.hooksPath .githooks
    printf "\033[0;32m✓ git hooks configured (.githooks/pre-push → just ci-quiet)\033[0m\n"
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
    if [ ! -d node_modules ] || [ ! -x node_modules/.bin/pagefind ] || [ ! -x node_modules/.bin/lhci ]; then
        printf "\033[0;31m✗ check failed: node_modules missing or incomplete\033[0m\n"
        printf "  Run: just init\n"
        echo ""
        exit 1
    fi
    printf "\033[0;32m✓ node_modules present with pagefind and lhci\033[0m\n"
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
    @rm -rf public resources .hugo_build.lock .lighthouseci reports/lighthouse
    @printf "\033[0;32m✓ clean completed successfully\033[0m\n"
    @echo ""

# Destroy build artifacts and server state
destroy:
    @echo ""
    @printf "\033[0;34m=== Destroying Build Artifacts ===\033[0m\n"
    @rm -rf public resources .hugo_build.lock .hugo-server.pid .hugo-server.log .lighthouseci reports/lighthouse
    @printf "\033[0;32m✓ destroy completed successfully\033[0m\n"
    @echo ""

# Start the Hugo development server
start:
    #!/usr/bin/env bash
    echo ""
    printf "\033[0;34m=== Starting Hugo Development Server ===\033[0m\n"
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

# Stop the Hugo development server
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
        printf "\033[0;31m✗ stop failed: no hugo server running on port {{port}}\033[0m\n"
        echo ""
        exit 1
    fi
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
            SOURCE="just dev"
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

# Run Hugo server in foreground with auto-rebuild + live-reload
dev:
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Hugo Dev Server (foreground, auto-rebuild + LiveReload) ===\033[0m\n"
    if [ -f .hugo-server.pid ] && kill -0 "$(cat .hugo-server.pid)" 2>/dev/null; then
        printf "\033[0;31m✗ dev failed: background server already running (PID %s). Run 'just stop' first.\033[0m\n" "$(cat .hugo-server.pid)"
        echo ""
        exit 1
    fi
    printf "\033[0;32m→ serving at http://127.0.0.1:{{port}}/  (Ctrl+C to stop)\033[0m\n"
    echo ""
    exec hugo server -D -F -E --bind 127.0.0.1 --port {{port}} --navigateToChanged --disableFastRender

# Fail if the working tree has uncommitted changes
check-clean-worktree:
    @echo ""
    @printf "\033[0;34m=== Checking Working Tree ===\033[0m\n"
    @bash scripts/check-clean-worktree.sh
    @printf "\033[0;32m✓ check-clean-worktree passed\033[0m\n"
    @echo ""

# Run ALL validation checks (verbose)
ci:
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Running CI Checks ===\033[0m\n"
    echo ""
    just check
    just build
    just validate-pagefind-index
    just check-clean-worktree
    just _run-lighthouse-checks
    echo ""
    printf "\033[0;32m✓ All CI checks passed\033[0m\n"
    echo ""

# Run ALL validation checks silently (only show output on errors)
ci-quiet:
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Running CI Checks (Quiet Mode) ===\033[0m\n"
    TMPFILE=$(mktemp)
    trap "rm -f $TMPFILE" EXIT

    just check > $TMPFILE 2>&1 || { printf "\033[0;31m✗ Check failed\033[0m\n"; cat $TMPFILE; exit 1; }
    printf "\033[0;32m✓ Check passed\033[0m\n"

    just build > $TMPFILE 2>&1 || { printf "\033[0;31m✗ Build failed\033[0m\n"; cat $TMPFILE; exit 1; }
    printf "\033[0;32m✓ Build passed\033[0m\n"

    just validate-pagefind-index > $TMPFILE 2>&1 || { printf "\033[0;31m✗ Pagefind validation failed\033[0m\n"; cat $TMPFILE; exit 1; }
    printf "\033[0;32m✓ Pagefind index valid\033[0m\n"

    just check-clean-worktree > $TMPFILE 2>&1 || { printf "\033[0;31m✗ Clean worktree check failed\033[0m\n"; cat $TMPFILE; exit 1; }
    printf "\033[0;32m✓ Working tree clean\033[0m\n"

    just _run-lighthouse-checks > $TMPFILE 2>&1 || { printf "\033[0;31m✗ Lighthouse CI failed\033[0m\n"; cat $TMPFILE; exit 1; }
    printf "\033[0;32m✓ Lighthouse CI passed\033[0m\n"

    echo ""
    printf "\033[0;32m✓ All CI checks passed\033[0m\n"
    echo ""

# Remove EXIF metadata from all images and videos in content/
strip-exif:
    @echo ""
    @printf "\033[0;34m=== Stripping EXIF Metadata ===\033[0m\n"
    @bash scripts/strip-exif.sh
    @printf "\033[0;32m✓ strip-exif completed\033[0m\n"
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

# Render Wardley map .wtg2 files to .svg using wtg2svg. Run locally after editing
# any .wtg2; commit the generated .svg alongside its source.
wardley-render:
    @echo ""
    @printf "\033[0;34m=== Rendering Wardley Maps → SVG ===\033[0m\n"
    @bash scripts/wardley-render.sh
    @printf "\033[0;32m✓ wardley-render completed\033[0m\n"
    @echo ""

# Check all image references in non-draft markdown resolve to files
validate-images:
    @echo ""
    @printf "\033[0;34m=== Validating Image References ===\033[0m\n"
    @bash scripts/validate-images.sh
    @printf "\033[0;32m✓ validate-images passed\033[0m\n"
    @echo ""

# Check unique external article links with curl, or a single Markdown file if given
check-links file='':
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Checking External Links ===\033[0m\n"
    if [ -n "{{file}}" ]; then
        python3 scripts/check-links.py --file "{{file}}"
    else
        python3 scripts/check-links.py content
    fi
    printf "\033[0;32m✓ check-links passed\033[0m\n"
    echo ""

# Check blog markdown for disallowed characters (em dashes)
validate-md:
    @echo ""
    @printf "\033[0;34m=== Validating Markdown (semgrep) ===\033[0m\n"
    @semgrep --config config/semgrep/no-em-dash.yml --error content
    @printf "\033[0;32m✓ validate-md passed\033[0m\n"
    @echo ""

# Check code blocks in draft articles for lines exceeding 76 characters (ignores mermaid/wardley)
check-code-line-length file='':
    @echo ""
    @printf "\033[0;34m=== Checking Code Block Line Lengths ===\033[0m\n"
    @bash scripts/check-code-line-length.sh {{file}}
    @printf "\033[0;32m✓ check-code-line-length passed\033[0m\n"
    @echo ""

# Fail when any draft article still contains unresolved TODO/placeholder markers
validate-content:
    @echo ""
    @printf "\033[0;34m=== Validating Draft Content ===\033[0m\n"
    @bash scripts/validate-content.sh
    @printf "\033[0;32m✓ validate-content passed\033[0m\n"
    @echo ""

# Spell check all draft articles (draft: true) with harper-cli, or a single file if given
spell-check file='':
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Spell Checking Draft Articles ===\033[0m\n"
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
    ERRORS=0
    while IFS= read -r file; do
        printf "\033[0;34m→ checking: %s\033[0m\n" "$file"
        harper-cli lint --user-dict-path config/harper/dictionary.txt "$file" || ERRORS=$((ERRORS + 1))
        echo ""
    done <<< "$DRAFTS"
    if [ "$ERRORS" -gt 0 ]; then
        printf "\033[0;31m✗ spell-check: %s file(s) reported issues\033[0m\n" "$ERRORS"
        echo ""
        exit 1
    fi
    printf "\033[0;32m✓ spell-check passed\033[0m\n"
    echo ""

# Build the production site (optimize → validate → hugo)
build:
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Building Production Site ===\033[0m\n"
    just optimize-images
    just strip-exif
    just validate-images
    just validate-content
    just check-code-line-length
    just validate-md
    hugo --minify --cleanDestinationDir
    just build-pagefind-index
    printf "\033[0;32m✓ build completed successfully\033[0m\n"
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

# Verify the Pagefind search index exists in public/ (tripwire against silent failures)
validate-pagefind-index:
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Validating Pagefind Search Index ===\033[0m\n"
    if [ ! -f public/pagefind/pagefind.js ] || [ ! -f public/pagefind/pagefind-entry.json ]; then
        printf "\033[0;31m✗ validate-pagefind-index failed: pagefind/ index missing or incomplete in public/\033[0m\n"
        printf "  Expected: public/pagefind/pagefind.js and public/pagefind/pagefind-entry.json\n"
        printf "  Fix: re-run 'just build' (or 'just build-pagefind-index' if public/ already exists)\n"
        echo ""
        exit 1
    fi
    printf "\033[0;32m✓ pagefind index present in public/pagefind/\033[0m\n"
    echo ""

# Build and run Lighthouse CI against public/ on an LHCI-managed temporary server
run-lighthouse-checks:
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Building and Running Lighthouse CI ===\033[0m\n"
    just build
    just _run-lighthouse-checks
    printf "\033[0;32m✓ run-lighthouse-checks completed successfully\033[0m\n"
    echo ""

# Remove generated Lighthouse CI reports
lighthouse-clean:
    @echo ""
    @printf "\033[0;34m=== Cleaning Lighthouse CI Reports ===\033[0m\n"
    @rm -rf .lighthouseci reports/lighthouse
    @printf "\033[0;32m✓ lighthouse-clean completed successfully\033[0m\n"
    @echo ""

# Open representative Lighthouse HTML reports
lighthouse-open:
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Opening Lighthouse CI Reports ===\033[0m\n"
    if [ ! -f reports/lighthouse/manifest.json ]; then
        printf "\033[0;31m✗ lighthouse-open failed: reports/lighthouse/manifest.json not found\033[0m\n"
        printf "  Run: just run-lighthouse-checks\n"
        echo ""
        exit 1
    fi
    REPORTS=$(node -e "const m=require('./reports/lighthouse/manifest.json'); console.log(m.filter(r=>r.isRepresentativeRun).map(r=>r.htmlPath).join('\n'))")
    if [ -z "$REPORTS" ]; then
        printf "\033[0;31m✗ lighthouse-open failed: no representative reports found\033[0m\n"
        echo ""
        exit 1
    fi
    while IFS= read -r report; do
        open "$report"
    done <<< "$REPORTS"
    printf "\033[0;32m✓ lighthouse reports opened\033[0m\n"
    echo ""

# Run Lighthouse CI against an already-built public/ directory
_run-lighthouse-checks:
    #!/usr/bin/env bash
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

# Deploy main to GitHub Pages (push if needed, watch run, verify live URL)
deploy: ci
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
