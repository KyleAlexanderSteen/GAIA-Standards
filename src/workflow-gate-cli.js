#!/usr/bin/env node
import { evaluateWorkflowFile } from "./workflow-gate.js";

function usage() {
  process.stderr.write("Usage: node src/workflow-gate-cli.js <manifest.json> --evaluation-time <ISO-8601> [--output <report.json>]\n");
}
const args = process.argv.slice(2);
const manifestPath = args[0];
const option = (name) => { const index = args.indexOf(name); return index >= 0 ? args[index + 1] : undefined; };
const evaluationTime = option("--evaluation-time");
const outputPath = option("--output");
if (!manifestPath || !evaluationTime || (args.includes("--output") && !outputPath)) {
  usage();
  process.exitCode = 2;
} else {
  try {
    const report = await evaluateWorkflowFile({ manifestPath, evaluationTime, outputPath });
    process.stdout.write(JSON.stringify(report, null, 2) + "\n");
    // Exit status means the input was evaluated without structural errors; it never authorizes release.
    process.exitCode = report.verdict === "invalid" ? 1 : 0;
  } catch (error) {
    process.stderr.write("Workflow gate failed safely: " + (error instanceof Error ? error.message : "unknown error") + "\n");
    process.exitCode = 1;
  }
}
