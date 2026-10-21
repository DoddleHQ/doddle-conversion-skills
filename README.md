# Doddle Conversion (CRO) Skills

**Doddle Conversion OS** — 30 agent-agnostic skills and 5 agents for conversion rate
optimization: strategy, research, landing pages, offers, experimentation, personalization and
measurement.

The one claim this pack makes: **every number is reproducible from recorded evidence.** A
stdlib-only Python toolkit (`dconv`) computes; the skills narrate and prioritize. Baseline
rates, MDEs and guardrails are assumptions and are always labelled `advisory`.

## Install

Point your agent at `.claude/skills/` and `.claude/agents/`, or install the DoddleOS plugin
from `.claude-plugin/plugin.json`.

```bash
python3 scripts/dconv doctor
python3 scripts/dconv version
```

Python 3.9+, no dependencies (stdlib only).

## The toolkit — `dconv`

```
dconv version
dconv frameworks [--name SLUG] [--json]
dconv ab-test --control-n N --control-conv C --variant-n N --variant-conv C [--json]
dconv sample-size --baseline R --mde D [--alpha A] [--power P] [--json]
dconv funnel --stage name:count ... [--json]
dconv landing-audit --checks '{...}' [--file F] [--json]
dconv offer --price P [--discount D] [--bundle JSON] [--json]
dconv doctor
```

## What is in the pack

**Skills (30)** grouped by the conversion motion:

| Group | Skills |
|-------|--------|
| Strategy & research | conv-strategy, cro-audit, cro-research, cro-heuristics, cro-copy, cro-ux |
| Landing pages | conv-landing-page, conv-landing-audit, cro-forms, cro-mobile, cro-speed, cro-trust |
| Offers & pricing | conv-offer-design, conv-pricing-page, conv-discount-strategy, conv-bundle-design, conv-guarantee |
| Experimentation | conv-experiment-design, conv-ab-testing, conv-multivariate, conv-hypothesis, conv-significance, conv-experiment-reporting |
| Personalization | conv-personalization, conv-segmentation, conv-dynamic-content, conv-geo-targeting |
| Measurement | conv-metrics, conv-funnel, conv-attribution |

**Agents (5):** `conversion-strategist`, `cro-analyst`, `ux-researcher`, `experiment-lead`,
`offer-strategist`.

Full inventory: [`skills-matrix.md`](skills-matrix.md). Authoring rules: [`AGENTS.md`](AGENTS.md).

## Validation

```bash
python3 scripts/lint_pack.py && python3 -m pytest tests -q
```

## License

MIT. See [`LICENSE`](LICENSE).
