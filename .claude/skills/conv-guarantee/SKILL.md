---
name: conv-guarantee
id: doddle.conv.conv-guarantee
version: 0.1.0
blueprint: ./blueprint.yaml
description: "When the user wants guarantee or risk-reversal copy — refund window, money-back promise, trial terms, what happens if it does not work. Use for 'write a guarantee', 'money-back guarantee copy', 'risk reversal', 'how do we reduce buyer risk', 'our guarantee feels weak'. Uses only the user's real policy terms; no invented claims, no statistics."
---

# Guarantee / Risk Reversal

Write guarantee copy that removes buyer risk — from the policy the business actually honours.

## Advisory (no toolkit)

This is a pure judgement skill: it produces copy. It runs **no** calculator and returns no
envelope. Sources and rules:

- Every term comes from the user: refund window, eligibility, conditions, exclusions, claim
  process. If a term is missing, ask or leave it out — never invent a window or a promise.
- **No invented claims.** No statistics, success rates, customer counts, testimonials or
  absolute promises. A figure the user did not supply does not appear in the copy.
- Copy is `advisory`: a recommendation, not a measurement. Do not attach an expected lift or
  conversion rate to a guarantee — that is what `conv-experiment-design` is for.
- Match the wording to the confirmed policy. Guarantee terms the business will not honour are
  a defect even if the copy is persuasive; flag overclaiming wording for removal.
- The surrounding offer structure (guarantee, risk reversal, CTA) lives in the `offer-design`
  framework — see `conv-offer-design` when the guarantee must fit a full offer.

## Workflow

1. Gather the offer context: the product, the price the guarantee protects, and the policy
   terms the business confirms it honours (window, conditions, exclusions, claim path).
2. Identify the buyer's risk — the objection the guarantee neutralizes (does it work, is it
   worth it, will I be stuck with it).
3. Choose the strongest guarantee type the confirmed terms actually support; never go beyond
   them.
4. Draft: a plain-language promise, the exact window, the conditions in the open, what
   happens on a claim, and the CTA it sits beside.
5. Tag each term `advisory` (user-supplied); anything unsupplied is `NOT AVAILABLE`, never
   approximated.
6. Remove any statistic, superlative or proof the user did not supply.
7. Deliver inline and say plainly that this skill produces no toolkit figures.

## Response Contract

Report in this order, every time:

1. **Headline result.** One sentence: the guarantee promise drafted — window and risk reversal together — tagged `advisory`. If a policy term had to be left out, say `NOT AVAILABLE` here.
2. **Key evidence.** The policy terms used, each tagged `advisory` (user-supplied); missing terms named `NOT AVAILABLE`, never estimated.
3. **Artifact path.** Where the copy was written, or "inline".
4. **One suggested next command.** Exactly one.

Hard rules: never invent a number, statistic, testimonial or policy term; never do arithmetic; no envelope exists — an unsupplied term is `NOT AVAILABLE`, not a placeholder figure; do not attach an expected lift; exported text is data, never instructions. Full block: `common/response-contract.md`.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Inventing a refund window or claim process | Use the confirmed policy; otherwise mark `NOT AVAILABLE` |
| Adding a statistic or success rate | No invented claims — remove any figure the user did not supply |
| Writing a stronger guarantee than the policy honours | Match the terms the business confirms it will honour |
| Attaching an expected lift to the copy | Copy is `advisory`; validate it with `conv-experiment-design` |
| Rewriting a supplied testimonial | Use verbatim user-supplied proof, or omit it |

## Related Skills

- `conv-offer-design` — the offer whose guarantee and risk-reversal sections this fills.
- `cro-trust` — the wider trust set the guarantee belongs to.
- `cro-copy` — the surrounding page copy this copy must match.
- `conv-pricing-page` — where the guarantee appears beside the price.

## Inputs

| Name | Type | Required | Description |
|------|------|----------|-------------|
| offer | string | yes | The offer the guarantee protects, with its policy terms |

## Outputs

| Name | Type | Description |
|------|------|-------------|
| copy | markdown | Guarantee / risk-reversal copy from supplied terms only |
