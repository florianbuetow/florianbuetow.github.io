#!/usr/bin/env node

import assert from "node:assert/strict";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";

const root = path.resolve(import.meta.dirname, "..");
const textlint = path.join(root, "node_modules", ".bin", "textlint");
const workDir = mkdtempSync(path.join(tmpdir(), "textlint-acronym-test-"));

function lint(name, markdown, options = {}) {
    const file = path.join(workDir, `${name}.md`);
    const config = path.join(workDir, `${name}.textlintrc.json`);
    writeFileSync(file, markdown, "utf8");
    writeFileSync(
        config,
        JSON.stringify({ rules: { "acronym-first-use": options } }),
        "utf8"
    );
    const result = spawnSync(
        textlint,
        [
            "--config",
            config,
            "--format",
            "json",
            file,
        ],
        { cwd: root, encoding: "utf8" }
    );
    assert.notEqual(result.status, null, result.error?.message);
    const reports = JSON.parse(result.stdout || "[]");
    return {
        status: result.status,
        messages: reports.flatMap((report) => report.messages),
        stderr: result.stderr,
    };
}

try {
    const expanded = lint(
        "expanded",
        "SDLC (Software Development Life Cycle) guides the work. The SDLC is useful."
    );
    assert.equal(expanded.status, 0, expanded.stderr);
    assert.equal(expanded.messages.length, 0);

    const compoundExpansion = lint(
        "compound-expansion",
        "SDLC (Software Development Lifecycle) guides the work."
    );
    assert.equal(compoundExpansion.status, 0, compoundExpansion.stderr);

    const missing = lint(
        "missing",
        "SDLC guides the work. The SDLC appears again."
    );
    assert.equal(missing.status, 1);
    assert.equal(missing.messages.length, 1);
    assert.match(missing.messages[0].message, /Expand SDLC on first use/);

    const expandedTooLate = lint(
        "expanded-too-late",
        "SDLC guides the work. SDLC (Software Development Life Cycle) is repeated."
    );
    assert.equal(expandedTooLate.status, 1);
    assert.equal(expandedTooLate.messages.length, 1);

    const invalidParentheses = lint(
        "invalid-parentheses",
        "SDLC (today) guides the work."
    );
    assert.equal(invalidParentheses.status, 1);

    const codeIsIgnored = lint(
        "code-is-ignored",
        "`SDLC`\n\n```text\nSDLC\n```\n"
    );
    assert.equal(codeIsIgnored.status, 0, codeIsIgnored.stderr);
    assert.equal(codeIsIgnored.messages.length, 0);

    const codeDoesNotCountAsFirstUse = lint(
        "code-before-prose",
        "`SDLC` appears in code.\n\nSDLC is unexplained in prose."
    );
    assert.equal(codeDoesNotCountAsFirstUse.status, 1);
    assert.equal(codeDoesNotCountAsFirstUse.messages.length, 1);

    const plural = lint(
        "plural",
        "APIs (Application Programming Interfaces) connect systems. APIs are reused."
    );
    assert.equal(plural.status, 0, plural.stderr);

    const configuredLengths = lint(
        "configured-lengths",
        "AI is short. TOOLONG is long. SDLC is in range.",
        { min_acronym_len: 3, max_acronym_len: 5 }
    );
    assert.equal(configuredLengths.status, 1);
    assert.equal(configuredLengths.messages.length, 1);
    assert.match(configuredLengths.messages[0].message, /Expand SDLC on first use/);

    const ignored = lint(
        "ignored",
        "SDLC is intentionally exempt here.",
        { ignore_acronyms: ["SDLC"] }
    );
    assert.equal(ignored.status, 0, ignored.stderr);
    assert.equal(ignored.messages.length, 0);

    console.log("✓ acronym-first-use textlint rule tests passed");
} finally {
    rmSync(workDir, { recursive: true, force: true });
}
