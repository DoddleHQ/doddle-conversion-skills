# Changelog

All notable changes to `doddle-conversion-skills` are documented here.

## [0.1.0] - 2026-10-21

First release. Doddle Conversion (CRO) OS — a standalone pack.

### Added

- **Deterministic toolkit** (`scripts/doddle_conversion/`, stdlib-only, Python 3.9+, CLI `dconv`):
  - `ab-test` (two-proportion z-test), `sample-size`, `funnel`, `landing-audit` (0-100, 10 checks),
    `offer` (discounts, bundles), `frameworks` (12 named templates), `version`, `doctor`;
  - a shared JSON evidence envelope (`envelope.py`).
- **30 skills** (`.claude/skills/`), hybrid agent-agnostic `SKILL.md` + DoddleOS `blueprint.yaml`.
- **5 agents** (`.claude/agents/`): `conversion-strategist`, `cro-analyst`, `ux-researcher`,
  `experiment-lead`, `offer-strategist`.
- **Shared references** (`.claude/skills/common/`): `response-contract.md`,
  `data-reliability.md`, `fundamentals.md`, `scoring-methodology.md`, `frameworks-registry.md`,
  `mcp-integration-guide.md`.
- **Manifests**: `plugin.json`, `marketplace.json`, `package.json`.
- **Validation**: `scripts/lint_pack.py` and the pytest suite (toolkit + pack), plus CI.
- **Docs**: `README.md`, `skills-matrix.md`, `AGENTS.md`.

### Principles

- Deterministic first: the toolkit computes, skills narrate.
- Assumptions (baseline rates, MDEs, guardrails) are labelled `advisory`.
- `null` means not measured, never zero.
- No hardcoded market statistics (linter-enforced).
- Read-only: no CRM writes, sends or ad-spend actions.

[0.1.0]: https://github.com/DoddleHQ/doddle-conversion-skills/releases/tag/v0.1.0
EOF
echo done