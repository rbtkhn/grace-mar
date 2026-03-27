#!/usr/bin/env node
/**
 * Interactive pre-commit style gate. Skips when CI=true or --yes.
 */
const readline = require("readline");

const skip =
  process.env.CI === "true" ||
  process.argv.includes("--yes") ||
  process.argv.includes("-y");

const questions = [
  "Does this change preserve core intention? (y/N)",
  "Have you validated record boundaries (python3 scripts/validate-record-boundaries.py)? (y/N)",
  "Confirm there is no forbidden layer crossing (per docs/layer-map.json). (y/N)",
];

async function runGate() {
  if (skip) {
    console.log("gate-guardian: skipped (CI or --yes)");
    process.exit(0);
  }
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  const ask = (q) =>
    new Promise((resolve) => rl.question(q + " ", resolve));

  console.log("\n=== RECURSION GATE (human) ===\n");
  for (const q of questions) {
    const answer = (await ask(q)).trim().toLowerCase();
    if (answer !== "y") {
      console.log("Gate blocked.");
      rl.close();
      process.exit(1);
    }
  }
  rl.close();
  console.log("Gate passed.");
}

runGate().catch((e) => {
  console.error(e);
  process.exit(1);
});
