# MCP Integration Guide & Tool Registry

Skills may reference external data only through tool IDs on this registry. Never invent a
tool ID. The toolkit CLI (`doddle.tool.cli.dconv`) covers everything deterministic.

## Registry

| Tool ID | Provides | Typical skills | Required |
|---------|----------|----------------|----------|
| `doddle.tool.cli.dconv` | A/B significance, sample size, landing audit, offer math, funnel, frameworks | all `conv-*` | yes (bundled) |
| `doddle.tool.v1.ga4.getReport` | Sessions, conversions, funnel drop-off by page | conv-metrics, conv-funnel, conv-attribution | no |
| `doddle.tool.v1.hubspot.contacts` | Lifecycle stage, lead score | conv-personalization, conv-segmentation | no |
| `doddle.tool.v1.clearbit.company` | Firmographic enrichment for personalization | conv-personalization, conv-segmentation | no |
| `doddle.tool.v1.notion.pages` | Experiment docs, CRO playbooks | conv-experiment-design, conv-enablement | no |
| `doddle.tool.v1.canva.design` | Design assets for variants | conv-creative, conv-landing-page | no |

## Rules

1. Deterministic first.
2. Optional tools are optional (`required: false`, `fallback: manual_review`).
3. Unavailable => say `⚠️ NOT AVAILABLE — configure <tool>`.
4. Live numbers are `live` class.
5. Never put API keys on a command line.
6. Read-only: no CRM writes, no sends, no ad spend.
