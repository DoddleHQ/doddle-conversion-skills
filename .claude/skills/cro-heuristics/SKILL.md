---
name: cro-heuristics
id: doddle.conv.cro-heuristics
version: 0.1.0
blueprint: ./blueprint.yaml
description: "When the user wants a LIFT heuristic review of a page — value proposition, relevance, clarity, urgency, anxiety, distraction. Use for 'LIFT review', 'heuristic evaluation', 'diagnose this page', 'why does this page feel weak', 'heuristic CRO check'."
---

# LIFT Heuristic Review

Diagnose a page against the LIFT model — structure from the registry, observations from the page.

## Deterministic Toolkit

```
dconv frameworks --name cro-heuristics --json
```

Read `frameworks[0].sections` — the exact LIFT structure to review:

1. Value proposition
2. Relevance
3. Clarity
4. Urgency
5. Anxiety (trust)
6. Distraction

The framework supplies the **structure** (from the registry, `deterministic`); every
observation about the page is `heuristic` — an expert judgement, never a measurement. If
`ok: false`, relay `error.message` and `error.hint`; check the `Known:` hint for valid slugs.

## Workflow

1. Pull the LIFT structure with `dconv frameworks --name cro-heuristics`.
2. Get the page from the user — paste, description or screenshots. Never review a page you
   have not seen; if there is no content, ask for it.
3. Assess each LIFT factor against the page content; each observation tagged `heuristic`.
4. Rank the factors by impact and confidence; state what evidence is still missing.
5. Recommend hand-offs: trust → `cro-trust`, copy → `cro-copy`, friction → `cro-ux`.
6. State `scoring_version`, `data_version` and `evidence.stamp` from the envelope.

## Response Contract

Report in this order, every time:

1. **Headline result.** One sentence: the weakest LIFT factor and why — tagged `heuristic`.
   If `evidence.stamp` is not `CURRENT`, say so here.
2. **Key evidence.** The per-factor observations, each tagged `heuristic`; anything not
   observable from the supplied page is `null`, not assumed.
3. **Artifact path.** Where the review was written, or "inline".
4. **One suggested next command.** Exactly one.

Hard rules: never invent a number; `null` is not measured, not zero; never do arithmetic;
observations are `heuristic`, the structure is `deterministic`; on `ok: false` relay
`error.message` + `error.hint`. Full block: `common/response-contract.md`.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Paraphrasing LIFT from memory | Read sections from `dconv frameworks` |
| Presenting a heuristic score as measured | There is no score; it is judgement, tagged `heuristic` |
| Reviewing a page you have not seen | Ask for the content first |
| Inventing user evidence | Observations come from the page only; research is `cro-research` |
| Skipping a factor because it looks fine | Assess all six; note why a factor is strong |

## Related Skills

- `cro-audit` — the full audit this review feeds.
- `cro-copy` — fix clarity and value-proposition findings with copy.
- `cro-trust` — deepen the anxiety (trust) factor.
- `cro-ux` — friction and distraction findings with the toolkit score.

## Inputs

| Name | Type | Required | Description |
|------|------|----------|-------------|
| page | string | yes | Page to review (content supplied by the user) |

## Outputs

| Name | Type | Description |
|------|------|-------------|
| review | markdown | LIFT heuristic review |
