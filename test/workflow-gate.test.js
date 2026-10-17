import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { evaluateWorkflowManifest } from "../src/workflow-gate.js";
const fixture = async (name) => readFile(new URL("./fixtures/" + name, import.meta.url), "utf8");
const time = "2026-10-17T00:00:00.000Z";

test("same bytes and pinned evaluation time produce equivalent reports", async () => {
  const manifestText = await fixture("workflow-valid-but-unverified.json");
  const first = await evaluateWorkflowManifest({ manifestText, evaluationTime: time });
  const second = await evaluateWorkflowManifest({ manifestText, evaluationTime: time });
  assert.deepEqual(first, second);
  assert.equal(first.evaluatedAt, time);
  for (const key of ["manifest", "schema", "registry"]) assert.equal(first.hashes[key].length, 64);
});

test("provisional inventory and untrusted identity fail closed", async () => {
  const report = await evaluateWorkflowManifest({ manifestText: await fixture("workflow-valid-but-unverified.json"), evaluationTime: time });
  assert.equal(report.layers.structuralValidity, "valid");
  assert.equal(report.verdict, "blocked");
  assert.equal(report.layers.releaseAuthorization, "not-authorized");
  for (const id of ["GATE-01", "GATE-06", "AUTH-001"]) assert.ok(report.findings.some((f) => f.ruleId === id));
  assert.notEqual(report.verdict, "release_authorized");
});

test("unsupported versions cannot produce a passing verdict", async () => {
  const report = await evaluateWorkflowManifest({ manifestText: await fixture("workflow-invalid-version.json"), evaluationTime: time });
  assert.equal(report.verdict, "invalid");
  assert.ok(report.findings.some((f) => f.ruleId === "VERSION-001"));
});

test("malformed JSON is invalid", async () => {
  const report = await evaluateWorkflowManifest({ manifestText: "{bad json", evaluationTime: time });
  assert.equal(report.verdict, "invalid");
  assert.equal(report.hashes.manifest.length, 64);
  assert.ok(report.findings.some((f) => f.ruleId === "MANIFEST-001"));
});

test("missing falsifiable acceptance criteria causes structural failure", async () => {
  const source = JSON.parse(await fixture("workflow-valid-but-unverified.json"));
  source.spec.goal.acceptance_tests[0].falsifiable = false;
  const report = await evaluateWorkflowManifest({ manifestText: JSON.stringify(source), evaluationTime: time });
  assert.equal(report.verdict, "invalid");
  assert.ok(report.findings.some((f) => f.ruleId === "SCHEMA-011"));
});

test("self-supersession is rejected", async () => {
  const source = JSON.parse(await fixture("workflow-valid-but-unverified.json"));
  source.metadata.supersedes = source.metadata.id;
  const report = await evaluateWorkflowManifest({ manifestText: JSON.stringify(source), evaluationTime: time });
  assert.equal(report.verdict, "invalid");
  assert.ok(report.findings.some((f) => f.ruleId === "REF-001"));
});

test("not-applicable controls require justification", async () => {
  const source = JSON.parse(await fixture("workflow-valid-but-unverified.json"));
  source.controls.privacy = { applicable: false };
  const report = await evaluateWorkflowManifest({ manifestText: JSON.stringify(source), evaluationTime: time });
  assert.equal(report.verdict, "blocked");
  assert.ok(report.findings.some((f) => f.ruleId === "APPL-001"));
});

test("evaluation time is mandatory and caller-pinned", async () => {
  await assert.rejects(() => evaluateWorkflowManifest({ manifestText: "{}", evaluationTime: undefined }), /evaluationTime/);
});

test("a deliberate invariant mutation is detected", async () => {
  const source = JSON.parse(await fixture("workflow-valid-but-unverified.json"));
  delete source.spec.goal.non_goals;
  const report = await evaluateWorkflowManifest({ manifestText: JSON.stringify(source), evaluationTime: time });
  assert.equal(report.verdict, "invalid");
  assert.ok(report.findings.some((f) => f.ruleId === "SCHEMA-012"));
});
