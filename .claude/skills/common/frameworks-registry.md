# Framework Registry

Named templates live in `scripts/doddle_conversion/frameworks.py`, versioned as one unit
(`conversion-frameworks-2026-10`). A framework is a *structure*, not a market figure.

Always read sections from the toolkit: `dconv frameworks --name <slug>`.

## Registered frameworks

| Slug | Name | Purpose |
|------|------|---------|
| `landing-page-anatomy` | Landing Page Anatomy | Structure a high-converting landing page |
| `ab-test-brief` | A/B Test Brief | Design a test before it runs |
| `cro-heuristics` | CRO Heuristics (LIFT) | Diagnose a page with the LIFT model |
| `offer-design` | Offer Design | Design an offer that converts |
| `form-optimization` | Form Optimization | Reduce friction in a form |
| `pricing-page` | Pricing Page | Structure a pricing page |
| `personalization` | Personalization Plan | Plan 1:1 or segment-level personalization |
| `experimentation-program` | Experimentation Program | Run experimentation as a program |
| `trust-signals` | Trust Signals | Catalog trust elements for a page |
| `mobile-conversion` | Mobile Conversion | Optimize conversion on mobile |
| `funnel-diagnosis` | Funnel Diagnosis | Diagnose a conversion funnel |
| `cro-audit` | CRO Audit | Full conversion audit of a page or flow |

## Rules

1. Structure from the registry, content from inputs.
2. Never invent a framework.
3. Bump `data_version` when frameworks change.
