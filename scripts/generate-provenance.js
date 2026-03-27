#!/usr/bin/env node
/**
 * Summarize mtimes for markdown under users/ and docs/ only.
 */
const fs = require("fs");
const path = require("path");

const REPO = path.resolve(__dirname, "..");
const OUT = path.join(REPO, "state", "provenance", "record-docs-summary.json");
const roots = [path.join(REPO, "users"), path.join(REPO, "docs")];

const provenance = { generatedAt: new Date().toISOString(), files: {} };

function scanDir(dir) {
  if (!fs.existsSync(dir)) return;
  for (const name of fs.readdirSync(dir)) {
    const full = path.join(dir, name);
    const st = fs.statSync(full);
    if (st.isDirectory()) {
      if (name === "node_modules") continue;
      scanDir(full);
    } else if (full.endsWith(".md")) {
      const rel = path.relative(REPO, full);
      provenance.files[rel] = {
        lastModified: st.mtime.toISOString(),
        size: st.size,
      };
    }
  }
}

for (const r of roots) scanDir(r);
fs.mkdirSync(path.dirname(OUT), { recursive: true });
fs.writeFileSync(OUT, JSON.stringify(provenance, null, 2));
console.log("Wrote", OUT);
