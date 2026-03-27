#!/usr/bin/env node
/**
 * Template integrity checker: all paths in template-manifest.json exist;
 * optional check that .DS_Store is not tracked.
 * Exit 0 if valid; 1 if something is wrong.
 *
 * Usage: node scripts/validate-template.js
 * Run from repo root.
 *
 * See docs/feedback-template-repo-evaluation.md (Action H1).
 */

const path = require("path");
const fs = require("fs");
const { execSync } = require("child_process");

const REPO_ROOT = path.resolve(__dirname, "..");
const MANIFEST_PATH = path.join(REPO_ROOT, "template-manifest.json");

function main() {
  let failed = false;

  if (!fs.existsSync(MANIFEST_PATH)) {
    console.error("template-manifest.json not found at repo root");
    process.exit(1);
  }

  const manifest = JSON.parse(fs.readFileSync(MANIFEST_PATH, "utf-8"));
  const paths = manifest.paths || [];

  for (const entry of paths) {
    const p = path.join(REPO_ROOT, entry.path);
    if (!fs.existsSync(p)) {
      console.error(`Missing path: ${entry.path}`);
      failed = true;
    }
  }

  try {
    const out = execSync("git ls-files", { encoding: "utf-8", cwd: REPO_ROOT });
    const tracked = out.split(/\n/).filter(Boolean);
    const dsStore = tracked.filter((f) => f.endsWith(".DS_Store") || f.includes("/.DS_Store"));
    if (dsStore.length > 0) {
      console.error("Forbidden tracked files (add to .gitignore and run 'git rm --cached'):", dsStore.join(", "));
      failed = true;
    }
  } catch (_) {
    // not a git repo or git not available; skip
  }

  if (failed) process.exit(1);
  console.log("validate-template: all manifest paths exist; no forbidden files tracked.");

  try {
    execSync("python3 scripts/validate-record-boundaries.py", {
      cwd: REPO_ROOT,
      stdio: "inherit",
    });
  } catch (_) {
    failed = true;
  }
  try {
    execSync("python3 scripts/layer-enforcer.py", { cwd: REPO_ROOT, stdio: "inherit" });
  } catch (_) {
    failed = true;
  }

  if (failed) process.exit(1);
}

main();
