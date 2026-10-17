import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { dirname, resolve, sep } from "node:path";

export const VALIDATOR_VERSION = "0.1.0";
export const MANIFEST_STATES = Object.freeze(["invalid", "blocked", "unverified", "not_applicable", "passed", "release_authorized"]);
const CONTROL_IDS = Object.freeze(["provenance", "versioning", "testing", "security", "privacy", "human_approval", "observability", "resilience", "learning"]);
const HERE = dirname(fileURLToPath(import.meta.url));
const SCHEMA_PATH = resolve(HERE, "../schemas/workflow-manifest.v1.json");
const REGISTRY_PATH = resolve(HERE, "../registry/control-inventory.v1.json");
const sha256 = (value) => createHash("sha256").update(value).digest("hex");
const isObject = (value) => value !== null && typeof value === "object" && !Array.isArray(value);
const nonEmpty = (value) => typeof value === "string" && value.trim().length > 0;
const finding = (ruleId, severity, message, path = "$") => ({ ruleId, severity, message, path });

/**
 * Stage A local evaluator. No network calls, dynamic schema fetches, or release authorization.
 * evaluationTime is mandatory and pinned by the caller for deterministic evaluation.
 */
export async function evaluateWorkflowManifest({ manifestText, evaluationTime }) {
  if (typeof evaluationTime !== "string" || Number.isNaN(Date.parse(evaluationTime))) {
    throw new TypeError("evaluationTime must be a valid ISO-8601 timestamp supplied by the caller");
  }
  const evaluatedAt = new Date(Date.parse(evaluationTime)).toISOString();
  const [schemaText, registryText] = await Promise.all([readFile(SCHEMA_PATH, "utf8"), readFile(REGISTRY_PATH, "utf8")]);
  const registry = JSON.parse(registryText);
  const findings = [];
  let manifest = null;
  let structuralValid = true;

  if (typeof manifestText !== "string") {
    structuralValid = false;
    findings.push(finding("MANIFEST-001", "error", "Manifest input must be UTF-8 JSON text."));
  } else {
    try { manifest = JSON.parse(manifestText); }
    catch {
      structuralValid = false;
      findings.push(finding("MANIFEST-001", "error", "Manifest is not valid JSON."));
    }
  }
  const manifestHash = typeof manifestText === "string" ? sha256(manifestText) : null;
  const controlResults = [];

  if (structuralValid) {
    const errors = validateShape(manifest);
    for (const item of errors) findings.push(finding(item.ruleId, "error", item.message, item.path));
    if (errors.length) structuralValid = false;
  }
  if (structuralValid && manifest.metadata.supersedes && manifest.metadata.supersedes === manifest.metadata.id) {
    findings.push(finding("REF-001", "error", "A workflow cannot supersede itself.", "$.metadata.supersedes"));
    structuralValid = false;
  }

  if (structuralValid) {
    if (manifest.spec.scope.exempt === true) {
      if (!nonEmpty(manifest.spec.scope.justification)) findings.push(finding("EXEMPT-001", "blocking", "Workflow exemption requires a non-empty justification.", "$.spec.scope.justification"));
      if (!nonEmpty(manifest.spec.scope.approver)) findings.push(finding("EXEMPT-002", "blocking", "Workflow exemption requires a named approver; this prototype cannot verify identity.", "$.spec.scope.approver"));
      findings.push(finding("EXEMPT-003", "blocking", "Exemption eligibility depends on unresolved owner policy and trusted classification evidence."));
    }
    for (const id of CONTROL_IDS) {
      const control = manifest.controls[id];
      if (control.applicable === false) {
        if (!nonEmpty(control.justification)) {
          controlResults.push({ id, state: "failed", findings: ["APPL-001"] });
          findings.push(finding("APPL-001", "blocking", "A not-applicable control requires a justification.", "$.controls." + id + ".justification"));
        } else {
          controlResults.push({ id, state: "not_applicable", findings: [] });
        }
      } else {
        controlResults.push({ id, state: "unverified", findings: ["EVID-001"] });
        findings.push(finding("EVID-001", "blocking", "Evidence cannot be independently verified by a trusted identity provider in Stage A; declarations alone cannot pass a control.", "$.controls." + id));
      }
    }
  }

  if (registry.status !== "approved" || registry.controls.length !== 10) {
    findings.push(finding("GATE-01", "blocking", "Canonical control inventory is unresolved: the specification requires ten controls but only nine are enumerated. No missing control is invented."));
  }
  findings.push(finding("GATE-06", "blocking", "Trusted identity and independent-verifier attestation are not configured; string identifiers are not proof of identity."));
  findings.push(finding("AUTH-001", "blocking", "Release authorization is disabled in Stage A. A report or exit code cannot authorize release."));

  const hasError = () => findings.some((item) => item.severity === "error");
  const hasBlocking = findings.some((item) => item.severity === "blocking");
  let verdict = !structuralValid || hasError() ? "invalid"
    : hasBlocking ? "blocked"
    : controlResults.some((item) => item.state === "unverified") ? "unverified" : "passed";

  // The example uses "draft" even though the specification describes six derived states.
  // Treat draft as authoring metadata; compare only recognized derived-state declarations.
  if (manifest?.status?.state && MANIFEST_STATES.includes(manifest.status.state) && manifest.status.state !== verdict) {
    findings.push(finding("STATE-001", "error", "Declared status.state disagrees with the derived verdict.", "$.status.state"));
    verdict = "invalid";
  }
  const finalVerdict = hasError() ? "invalid" : verdict;
  return {
    reportVersion: "1.0.0",
    evaluatedAt,
    manifestId: isObject(manifest) && nonEmpty(manifest.metadata?.id) ? manifest.metadata.id : null,
    manifestVersion: isObject(manifest) && nonEmpty(manifest.metadata?.version) ? manifest.metadata.version : null,
    verdict: finalVerdict,
    layers: {
      structuralValidity: structuralValid ? "valid" : "invalid",
      evidenceValidity: !structuralValid ? "not-evaluated" : findings.some((item) => item.ruleId.startsWith("EVID-")) ? "unverified" : "valid",
      policyCompliance: hasBlocking ? "blocked" : "unverified",
      releaseAuthorization: "not-authorized"
    },
    findings: findings.sort((a, b) => a.ruleId.localeCompare(b.ruleId) || a.path.localeCompare(b.path) || a.message.localeCompare(b.message)),
    controlResults: controlResults.sort((a, b) => a.id.localeCompare(b.id)).map((item) => ({ ...item, findings: item.findings.sort() })),
    hashes: { validator: VALIDATOR_VERSION, schema: sha256(schemaText), registry: sha256(registryText), manifest: manifestHash },
    limitations: [
      "Stage A accepts JSON only; YAML parsing and version migration are not implemented.",
      "The control inventory remains unresolved and intentionally blocks a passing verdict.",
      "Evidence contents, evidence TTL policy, identity, and independent verification cannot be established by this local prototype.",
      "No trusted approval receipt is configured; release_authorized is never emitted.",
      "The report is deterministic for identical manifest bytes, registry/schema bytes, validator version, and pinned evaluationTime."
    ]
  };
}

function validateShape(manifest) {
  const errors = [];
  const required = (object, keys, path) => {
    for (const key of keys) if (!(key in object)) errors.push({ ruleId: "SCHEMA-001", message: "Missing required field: " + key, path: path + "." + key });
  };
  if (!isObject(manifest)) return [{ ruleId: "SCHEMA-001", message: "Manifest must be a JSON object.", path: "$" }];
  required(manifest, ["apiVersion", "kind", "metadata", "spec", "controls"], "$");
  if (manifest.apiVersion !== "gaia.dev/v1") errors.push({ ruleId: "VERSION-001", message: "Unknown or unsupported apiVersion; expected gaia.dev/v1.", path: "$.apiVersion" });
  if (manifest.kind !== "WorkflowManifest") errors.push({ ruleId: "SCHEMA-002", message: "kind must equal WorkflowManifest.", path: "$.kind" });
  const metadata = manifest.metadata;
  if (!isObject(metadata)) errors.push({ ruleId: "SCHEMA-003", message: "metadata must be an object.", path: "$.metadata" });
  else {
    required(metadata, ["id", "name", "version", "owner", "domain"], "$.metadata");
    if (typeof metadata.id !== "string" || !/^WF-[A-Z0-9]+-[0-9]{3}$/.test(metadata.id)) errors.push({ ruleId: "SCHEMA-004", message: "metadata.id does not match the required workflow ID pattern.", path: "$.metadata.id" });
    if (!nonEmpty(metadata.name) || !nonEmpty(metadata.owner) || !nonEmpty(metadata.domain)) errors.push({ ruleId: "SCHEMA-005", message: "metadata.name, owner, and domain must be non-empty strings.", path: "$.metadata" });
    if (typeof metadata.version !== "string" || !/^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(-[0-9A-Za-z.-]+)?(\+[0-9A-Za-z.-]+)?$/.test(metadata.version)) errors.push({ ruleId: "SCHEMA-006", message: "metadata.version must be semantic versioning.", path: "$.metadata.version" });
  }
  const spec = manifest.spec;
  if (!isObject(spec)) errors.push({ ruleId: "SCHEMA-007", message: "spec must be an object.", path: "$.spec" });
  else {
    for (const field of ["scope", "goal"]) if (!isObject(spec[field])) errors.push({ ruleId: "SCHEMA-008", message: "spec." + field + " must be an object.", path: "$.spec." + field });
    if (isObject(spec.scope) && typeof spec.scope.exempt !== "boolean") errors.push({ ruleId: "SCHEMA-009", message: "spec.scope.exempt must be boolean.", path: "$.spec.scope.exempt" });
    if (isObject(spec.goal)) {
      if (!nonEmpty(spec.goal.statement)) errors.push({ ruleId: "SCHEMA-010", message: "Goal statement must be non-empty.", path: "$.spec.goal.statement" });
      if (!Array.isArray(spec.goal.acceptance_tests) || spec.goal.acceptance_tests.length === 0 || spec.goal.acceptance_tests.some((t) => !isObject(t) || !nonEmpty(t.id) || !nonEmpty(t.statement) || t.falsifiable !== true)) errors.push({ ruleId: "SCHEMA-011", message: "At least one acceptance test with id, statement, and falsifiable=true is required.", path: "$.spec.goal.acceptance_tests" });
      else if (new Set(spec.goal.acceptance_tests.map((t) => t.id)).size !== spec.goal.acceptance_tests.length) errors.push({ ruleId: "REF-002", message: "Acceptance test IDs must be unique within a workflow manifest.", path: "$.spec.goal.acceptance_tests" });
      if (!Array.isArray(spec.goal.non_goals) || spec.goal.non_goals.length === 0 || spec.goal.non_goals.some((v) => !nonEmpty(v))) errors.push({ ruleId: "SCHEMA-012", message: "At least one explicit non-goal is required.", path: "$.spec.goal.non_goals" });
    }
    for (const key of ["inputs", "outputs"]) {
      if (!Array.isArray(spec[key]) || spec[key].length === 0 || spec[key].some((a) => !isObject(a) || !nonEmpty(a.id) || !nonEmpty(a.schema_uri) || !nonEmpty(a.version))) errors.push({ ruleId: "SCHEMA-013", message: "spec." + key + " must contain at least one artifact with id, schema_uri, and version.", path: "$.spec." + key });
    }
  }
  if (!isObject(manifest.controls)) errors.push({ ruleId: "SCHEMA-014", message: "controls must be an object.", path: "$.controls" });
  else {
    for (const id of CONTROL_IDS) {
      if (!isObject(manifest.controls[id])) errors.push({ ruleId: "SCHEMA-015", message: "Required control block is missing or malformed: " + id + ".", path: "$.controls." + id });
      else if (typeof manifest.controls[id].applicable !== "boolean") errors.push({ ruleId: "SCHEMA-016", message: "Control applicable must be boolean.", path: "$.controls." + id + ".applicable" });
    }
    const unknown = Object.keys(manifest.controls).filter((id) => !CONTROL_IDS.includes(id));
    if (unknown.length) errors.push({ ruleId: "SCHEMA-017", message: "Unknown control block(s): " + unknown.sort().join(", "), path: "$.controls" });
  }
  if (manifest.waivers !== undefined && !Array.isArray(manifest.waivers)) errors.push({ ruleId: "SCHEMA-018", message: "waivers must be an array when supplied.", path: "$.waivers" });
  return errors;
}

export async function evaluateWorkflowFile({ manifestPath, evaluationTime, outputPath }) {
  const absoluteManifest = resolve(manifestPath);
  const manifestText = await readFile(absoluteManifest, "utf8");
  const report = await evaluateWorkflowManifest({ manifestText, evaluationTime });
  if (outputPath) {
    const out = resolve(outputPath);
    const allowedRoot = resolve(process.env.GAIA_GATE_OUTPUT_DIR ?? process.cwd());
    if (out !== allowedRoot && !out.startsWith(allowedRoot + sep)) throw new Error("Output path must remain inside GAIA_GATE_OUTPUT_DIR or the current working directory.");
    const { mkdir, writeFile } = await import("node:fs/promises");
    await mkdir(dirname(out), { recursive: true });
    await writeFile(out, JSON.stringify(report, null, 2) + "\n", { flag: "wx" });
  }
  return report;
}
