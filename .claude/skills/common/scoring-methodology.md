# Scoring & Calculation Methodology

Versions: `scoring_version` (`conv-1`) and `data_version` (`conversion-frameworks-2026-10`).

## Calculators

| Command | Formula | Notes |
|---------|---------|-------|
| `dconv ab-test` | two-proportion z-test; p-value two-sided; winner by significance + direction | needs counts, not rates |
| `dconv sample-size` | standard formula, pooled variance, two-sided | per-arm and total |
| `dconv funnel` | step conversion = count[i]/count[i-1]; overall = last/first | zero stage -> null |
| `dconv landing-audit` | weighted 0-100 over recorded checks; missing checks skipped | readiness, not performance |
| `dconv offer` | discounted price, savings, bundle value, effective discount | |

## Landing audit (0-100, 10 checks)

clear_headline(15), single_cta(15), cta_above_fold(10), form_fields_le_3(10), trust_signals(10),
mobile_friendly(10), fast_load(10), message_match(10), social_proof(5), no_distractions(5).

Tier bands: Excellent >=85, Good >=70, Fair >=55, Weak >=40, Critical <40.

## Rules

1. Pure function of recorded input. Same input -> same output.
2. `null` never counts as zero; it leaves the denominator.
3. Findings carry `points_lost`.
4. Thresholds are documented starting lines, not benchmarks.
