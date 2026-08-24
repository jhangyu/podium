---
name: security-router
description: Use when the task involves security analysis or hardening. Security knowledge index — attack trees, threat paths, SAST tool configuration, DevSecOps vulnerability scanning, security requirements from threat models, security user stories, STRIDE methodology, threat modeling sessions, threat-to-control mapping, mitigation prioritization, remediation planning, dependency vulnerability scanning SBOM supply chain, security hardening defense-in-depth compliance, static analysis Bandit Semgrep CodeQL, XSS scanning frontend/mobile, compliance checks GDPR/SOC2/HIPAA.
---

# Security Router

This skill is an index. Identify the matching topic below, then Read the referenced file (path is relative to this SKILL.md's directory) and follow it. Read at most 2 references per task — if none match, say so rather than guessing.

| Topic | Reference | Use when |
|---|---|---|
| attack trees, threat paths, defense gaps | references/attack-tree-construction/SKILL.md | Mapping attack scenarios, communicating risk to stakeholders |
| SAST tool setup, vulnerability detection | references/sast-configuration.md | Setting up security scanning, automating code vuln detection |
| security requirements, user stories | references/security-requirement-extraction/SKILL.md | Translating threats into requirements or test cases |
| STRIDE, systematic threat identification | references/stride-analysis-patterns/SKILL.md | Analyzing system security, threat modeling sessions |
| threat-to-control mapping, remediation plans | references/threat-mitigation-mapping/SKILL.md | Prioritizing security investments, validating controls |

| dependency vulnerability scanning, SBOM, supply chain | references/security-dependencies.md | Scanning deps for CVEs, generating SBOM, remediation planning |
| security hardening, defense-in-depth, compliance | references/security-hardening.md | End-to-end security hardening across all application layers |
| SAST, Bandit, Semgrep, CodeQL, static analysis | references/security-sast.md | Running static analysis tools, custom rule authoring, CI integration |
| XSS vulnerability scanning, frontend/mobile | references/xss-scan.md | Scanning frontend/mobile code for XSS attack vectors and fixes |
| compliance framework checks (GDPR, SOC2, HIPAA) | references/compliance-check.md | Checking a codebase against a compliance framework |

Note: security-compliance and backend-api-security plugins have no skills/ content (agent+command only) — nothing unique to index here from them.
