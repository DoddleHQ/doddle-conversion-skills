# Skills Matrix

30 skills, 5 agents. Toolkit: `dconv`. Framework slugs are read from `dconv frameworks`.

## Strategy & research (6)

| Skill | Agent | Toolkit | Purpose |
|-------|-------|---------|---------|
| `conv-strategy` | conversion-strategist | frameworks | Conversion program strategy |
| `cro-audit` | cro-analyst | landing-audit, frameworks (cro-audit) | Full conversion audit |
| `cro-research` | ux-researcher | advisory | User research for conversion |
| `cro-heuristics` | ux-researcher | frameworks (cro-heuristics) | LIFT heuristic review |
| `cro-copy` | conversion-strategist | advisory | Conversion copy |
| `cro-ux` | ux-researcher | landing-audit | UX friction review |

## Landing pages (6)

| Skill | Agent | Toolkit | Purpose |
|-------|-------|---------|---------|
| `conv-landing-page` | conversion-strategist | frameworks (landing-page-anatomy) | Build a landing page |
| `conv-landing-audit` | cro-analyst | landing-audit | Score a landing page |
| `cro-forms` | ux-researcher | frameworks (form-optimization) | Form optimization |
| `cro-mobile` | ux-researcher | frameworks (mobile-conversion) | Mobile conversion |
| `cro-speed` | cro-analyst | advisory | Page speed |
| `cro-trust` | ux-researcher | frameworks (trust-signals) | Trust signals |

## Offers & pricing (5)

| Skill | Agent | Toolkit | Purpose |
|-------|-------|---------|---------|
| `conv-offer-design` | offer-strategist | frameworks (offer-design) | Offer design |
| `conv-pricing-page` | offer-strategist | frameworks (pricing-page) | Pricing page |
| `conv-discount-strategy` | offer-strategist | offer | Discount strategy |
| `conv-bundle-design` | offer-strategist | offer | Bundle design |
| `conv-guarantee` | offer-strategist | advisory | Guarantee / risk reversal |

## Experimentation (6)

| Skill | Agent | Toolkit | Purpose |
|-------|-------|---------|---------|
| `conv-experiment-design` | experiment-lead | frameworks (ab-test-brief) | Experiment brief |
| `conv-ab-testing` | experiment-lead | ab-test | Run an A/B test |
| `conv-multivariate` | experiment-lead | frameworks (ab-test-brief) | Multivariate test |
| `conv-hypothesis` | experiment-lead | advisory | Hypothesis writing |
| `conv-significance` | experiment-lead | ab-test | Significance check |
| `conv-experiment-reporting` | experiment-lead | ab-test | Experiment report |

## Personalization (4)

| Skill | Agent | Toolkit | Purpose |
|-------|-------|---------|---------|
| `conv-personalization` | conversion-strategist | frameworks (personalization) | Personalization plan |
| `conv-segmentation` | conversion-strategist | advisory | Conversion segmentation |
| `conv-dynamic-content` | conversion-strategist | advisory | Dynamic content |
| `conv-geo-targeting` | conversion-strategist | advisory | Geo targeting |

## Measurement (3)

| Skill | Agent | Toolkit | Purpose |
|-------|-------|---------|---------|
| `conv-metrics` | cro-analyst | landing-audit, funnel | Conversion metrics |
| `conv-funnel` | cro-analyst | funnel | Funnel analysis |
| `conv-attribution` | cro-analyst | advisory | Attribution (lite) |

## Agents

| Agent | Owns |
|-------|------|
| `conversion-strategist` | The conversion program: strategy, backlog, offers, personalization |
| `cro-analyst` | Numbers: audits, tests, sample sizes, funnels, metrics |
| `ux-researcher` | Heuristics, forms, mobile, trust, friction |
| `experiment-lead` | Hypothesis, design, significance, reporting |
| `offer-strategist` | Offers, pricing pages, discounts, bundles, guarantees |
EOF
echo "matrix written"