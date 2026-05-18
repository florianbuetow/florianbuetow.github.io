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
    @printf "  %-18s %s\n" "optimize-images" "Convert PNG/JPG/JPEG to WebP (max 1440px, q99)"
    @printf "  %-18s %s\n" "validate-images" "Check all image references resolve to files"
    @printf "  %-18s %s\n" "build" "Build the production site (optimize → validate → hugo)"
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
    if [ ! -d node_modules ]; then
        printf "\033[0;33m→ node_modules missing, running 'npm install'...\033[0m\n"
        npm install
    fi
    printf "\033[0;32m✓ node_modules present\033[0m\n"
    if ! command -v cwebp >/dev/null 2>&1; then
        printf "\033[0;33m→ cwebp missing, installing webp via brew...\033[0m\n"
        brew install webp
    fi
    printf "\033[0;32m✓ cwebp ready (%s)\033[0m\n" "$(cwebp -version 2>&1 | head -1)"
    mkdir -p public
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
    if [ ! -d node_modules ]; then
        printf "\033[0;31m✗ check failed: node_modules not found\033[0m\n"
        printf "  Run: just init\n"
        echo ""
        exit 1
    fi
    printf "\033[0;32m✓ node_modules present\033[0m\n"
    if ! command -v cwebp >/dev/null 2>&1; then
        printf "\033[0;31m✗ check failed: cwebp is not installed\033[0m\n"
        printf "  Install with: brew install webp  (or run: just init)\n"
        echo ""
        exit 1
    fi
    printf "\033[0;32m✓ cwebp is installed (%s)\033[0m\n" "$(cwebp -version 2>&1 | head -1)"
    echo ""

# Clean generated files
clean:
    @echo ""
    @printf "\033[0;34m=== Cleaning Generated Files ===\033[0m\n"
    @rm -rf public resources .hugo_build.lock
    @printf "\033[0;32m✓ clean completed successfully\033[0m\n"
    @echo ""

# Destroy build artifacts and server state
destroy:
    @echo ""
    @printf "\033[0;34m=== Destroying Build Artifacts ===\033[0m\n"
    @rm -rf public resources .hugo_build.lock .hugo-server.pid .hugo-server.log
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

# Run ALL validation checks (verbose)
ci:
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Running CI Checks ===\033[0m\n"
    echo ""
    just check
    just build
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

    echo ""
    printf "\033[0;32m✓ All CI checks passed\033[0m\n"
    echo ""

# Convert PNG/JPG/JPEG to WebP (max 1440px longest side, quality 99, never upsize)
optimize-images:
    @echo ""
    @printf "\033[0;34m=== Optimizing Images → WebP ===\033[0m\n"
    @bash scripts/optimize-images.sh
    @printf "\033[0;32m✓ optimize-images completed\033[0m\n"
    @echo ""

# Check all image references in non-draft markdown resolve to files
validate-images:
    @echo ""
    @printf "\033[0;34m=== Validating Image References ===\033[0m\n"
    @bash scripts/validate-images.sh
    @printf "\033[0;32m✓ validate-images passed\033[0m\n"
    @echo ""

# Build the production site (optimize → validate → hugo)
build:
    #!/usr/bin/env bash
    set -e
    echo ""
    printf "\033[0;34m=== Building Production Site ===\033[0m\n"
    just optimize-images
    just validate-images
    hugo --minify
    printf "\033[0;32m✓ build completed successfully\033[0m\n"
    echo ""

# Deploy main to GitHub Pages (push if needed, watch run, verify live URL)
deploy:
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
