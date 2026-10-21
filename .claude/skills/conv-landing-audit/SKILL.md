---
name: conv-landing-audit
id: doddle.conv.conv-landing-audit
version: 0.1.0
blueprint: ./blueprint.yaml
description: "When the user wants to score a landing page 0-100 from recorded checks — headline, CTA, form, trust, mobile, speed, message match. Use for 'audit this landing page', 'score my landing page', 'how does this page rate', 'run the landing checks', 'landing page review'."
---

# Landing Audit

Score a landing page 0-100 from recorded checks — reproducibly, never by feel.

## Deterministic Toolkit

```
dconv landing-audit --checks '{"clear_headline": true, "single_cta": true}' --json
dconv landing-audit --file checks.json --json
```

The ten checks and their fixed weights: `clear_headline` (15), `single_cta` (15),
`cta_above_fold` (10), `form_fields_le_3` (10), `trust_signals` (10), `mobile_friendly` (10),
`fast_load` (10), `message_match` (10), `social_proof` (5), `no_distractions` (5).

Read the JSON envelope — every figure comes from it:

- `metrics.score` / `scores.composite` / `scores.tier` — the 0-100 result and its band.
- `signals[]` — `landing.<check>` with `value`, `max`, `class` and `skipped_reason`.
- `findings[]` — failed checks, ordered, each with `points_lost` and `priority`.
- `completeness.signals` (`n/10`) and `metrics.checks_recorded` — coverage.
- `scoring_version`, `data_version`, `evidence.stamp`.

A check that was not recorded is `null` with a `skipped_reason`: it leaves the denominator, it
does not count as a failure. The score is weighted **readiness of the recorded checks, not
conversion performance** (tier bands in `common/scoring-methodology.md`). Optionally pull live
page context from `doddle.tool.v1.ga4.getReport` and tag it `live`; if unconfigured say
`⚠️ NOT AVAILABLE — configure doddle.tool.v1.ga4.getReport`.

## Workflow

1. Record the ten checks as booleans from evidence the user provides (page review, recordings,
   analytics). Never record a check you did not observe.
2. Run `dconv landing-audit --checks '<json>'`, or `--file checks.json` for a saved set.
3. If `ok: false`, relay `error.message` and `error.hint`; stop.
4. Narrate `metrics.score` with `scores.tier` in one sentence, then `findings[]` by
   `points_lost`.
5. Report every `null` signal with its `skipped_reason` as not measured.
6. State `scoring_version`, `data_version` and `evidence.stamp`.

## Response Contract

Report in this order, every time:

1. **Headline result.** One sentence carrying the score and the tier together (e.g. score 72,
   Good). If `evidence.stamp` is not `CURRENT`, say so here.
2. **Key evidence.** The checks that moved the score, each tagged `deterministic`; any GA4
   context tagged `live`; unrecorded checks named as `null` / not measured.
3. **Artifact path.** Where the JSON envelope and report were written, or "inline".
4. **One suggested next command.** Exactly one.

Hard rules: never invent a number; `null` is not measured, not zero; never do arithmetic — the
toolkit computes the score; assumptions are labelled, live numbers are `live`; on `ok: false`
relay `error.message` + `error.hint`. Full block: `common/response-contract.md`.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Recomputing the score by hand | Read `metrics.score` and `scores.tier` from the envelope |
| Marking an unobserved check `false` | Omit it; an unrecorded check is `null` and leaves the denominator |
| Reading `null` as a failed check | `null` is not measured; quote `skipped_reason` |
| Presenting the score as a conversion rate | It is weighted readiness over recorded checks, not performance |
| Benchmarking against quoted industry rates | Compare only the recorded checks; no market statistics |

## Related Skills

- `conv-landing-page` — build the page this skill scores.
- `cro-audit` — the full-page audit that uses this check set.
- `cro-heuristics` — the LIFT diagnosis behind a weak score.
- `cro-ux` — friction review of the recorded failures.
- `cro-speed` — advisory depth for the `fast_load` check.

## Inputs

| Name | Type | Required | Description |
|------|------|----------|-------------|
| checks | file/string | yes | Recorded check results as a JSON object (or a path via `--file`) |
| page | string | no | Page name or URL the checks refer to |

## Outputs

| Name | Type | Description |
|------|------|-------------|
| report | markdown | Landing audit report with prioritized findings |
| envelope | json | Audit envelope (score, tier, signals, findings) |
