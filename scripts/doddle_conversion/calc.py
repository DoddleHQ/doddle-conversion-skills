"""CRO calculators: A/B significance, sample size, landing-page audit, offer math, funnel."""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional

from . import DATA_VERSION, SCORING_VERSION, TOOLKIT_VERSION
from .envelope import CURRENT, Finding, Signal, make_envelope, tier_for


def _ratio(num: Optional[float], den: Optional[float]) -> Optional[float]:
    if num is None or den in (None, 0):
        return None
    return round(num / den, 6)


def ab_test(baseline_n: int, baseline_conv: int, variant_n: int, variant_conv: int) -> Dict[str, Any]:
    """Two-proportion z-test for an A/B test.

    Inputs are counts: visitors and conversions for each arm. Returns conversion rates,
    absolute/relative lift, z-score, p-value (two-sided), significance at 95%, and a
    Wilson 95% CI for the lift. No external stats library.
    """
    if baseline_n <= 0 or variant_n <= 0:
        return {"error": "sample sizes must be positive"}
    p0 = baseline_conv / baseline_n
    p1 = variant_conv / variant_n
    pooled = (baseline_conv + variant_conv) / (baseline_n + variant_n)
    se = math.sqrt(pooled * (1 - pooled) * (1 / baseline_n + 1 / variant_n))
    z = (p1 - p0) / se if se > 0 else 0.0
    # two-sided p-value via normal CDF (erf)
    p_value = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))
    lift_abs = p1 - p0
    lift_rel = (p1 - p0) / p0 if p0 > 0 else None
    # Wilson CI for the difference
    zc = 1.959963984540054
    se_diff = math.sqrt(p0 * (1 - p0) / baseline_n + p1 * (1 - p1) / variant_n)
    ci_lo = lift_abs - zc * se_diff
    ci_hi = lift_abs + zc * se_diff
    significant = p_value < 0.05
    winner = ("variant" if (significant and lift_abs > 0) else
              "control" if (significant and lift_abs < 0) else "inconclusive")
    return {
        "control": {"n": baseline_n, "conversions": baseline_conv, "rate": round(p0, 6)},
        "variant": {"n": variant_n, "conversions": variant_conv, "rate": round(p1, 6)},
        "lift_absolute": round(lift_abs, 6),
        "lift_relative": None if lift_rel is None else round(lift_rel, 6),
        "z_score": round(z, 4),
        "p_value": round(p_value, 6),
        "significant_at_95": significant,
        "winner": winner,
        "ci_95_lift": [round(ci_lo, 6), round(ci_hi, 6)],
        "notes": (["one arm has zero conversions; relative lift is undefined"]
                  if (baseline_conv == 0 or variant_conv == 0) else []),
    }


def sample_size(*, baseline_rate: float, mde: float, alpha: float = 0.05,
                power: float = 0.8) -> Dict[str, Any]:
    """Required sample size per arm for a two-proportion test.

    ``mde`` is the minimum detectable effect as an absolute rate difference (e.g. 0.02
    for a 2-point lift). Uses the standard formula with pooled variance.
    """
    if baseline_rate <= 0 or baseline_rate >= 1:
        return {"error": "baseline_rate must be in (0,1)"}
    if mde <= 0:
        return {"error": "mde must be positive"}
    p1 = baseline_rate + mde
    if p1 >= 1:
        return {"error": "baseline_rate + mde must be < 1"}
    # z values
    def z_for(p: float) -> float:
        # inverse normal via Abramowitz & Stegun approximation
        import math as _m
        if p <= 0 or p >= 1:
            return 0.0
        # use scipy-free: approximate with known quantiles for common alpha/power
        return _m.sqrt(2) * _erfinv(2 * p - 1)

    def _erfinv(x: float) -> float:
        # Acklam-ish approximation
        a = 0.147
        ln = math.log(1 - x * x)
        first = 2 / (math.pi * a) + ln / 2
        second = ln / a
        return math.copysign(math.sqrt(math.sqrt(first * first - second) - first), x)

    z_alpha = z_for(1 - alpha / 2)
    z_beta = z_for(power)
    p_bar = (baseline_rate + p1) / 2
    n = ((z_alpha * math.sqrt(2 * p_bar * (1 - p_bar)) +
          z_beta * math.sqrt(baseline_rate * (1 - baseline_rate) + p1 * (1 - p1))) ** 2) / (mde ** 2)
    return {
        "baseline_rate": baseline_rate,
        "target_rate": round(p1, 6),
        "mde_absolute": mde,
        "alpha": alpha,
        "power": power,
        "per_arm": math.ceil(n),
        "total": math.ceil(n) * 2,
        "notes": ["Assumes a two-sided test with equal allocation; adjust for one-sided or unequal splits."],
    }


def funnel(stages: List[Dict[str, Any]]) -> Dict[str, Any]:
    clean = [{"name": str(s.get("name", f"stage{i+1}")), "count": s.get("count")} for i, s in enumerate(stages)]
    steps: List[Dict[str, Any]] = []
    for i in range(1, len(clean)):
        prev, cur = clean[i - 1]["count"], clean[i]["count"]
        steps.append({"from": clean[i - 1]["name"], "to": clean[i]["name"],
                      "from_count": prev, "to_count": cur,
                      "conversion": _ratio(cur, prev),
                      "dropoff": None if (prev is None or cur is None) else prev - cur})
    overall = _ratio(clean[-1]["count"], clean[0]["count"]) if len(clean) >= 2 else None
    return {"stages": clean, "steps": steps, "overall_conversion": overall,
            "worst_step": (min((s for s in steps if s["conversion"] is not None), key=lambda s: s["conversion"])
                           if any(s["conversion"] is not None for s in steps) else None)}


def landing_audit(checks: Dict[str, Any]) -> Dict[str, Any]:
    """Score a landing page from recorded check results.

    ``checks`` is a dict of check-name -> bool (or 0/1). Weights are fixed and documented;
    a missing check is skipped (not counted as failed). Returns a 0-100 score, tier, and
    findings for failed checks.
    """
    weights = {
        "clear_headline": 15,
        "single_cta": 15,
        "cta_above_fold": 10,
        "form_fields_le_3": 10,
        "trust_signals": 10,
        "mobile_friendly": 10,
        "fast_load": 10,
        "message_match": 10,
        "social_proof": 5,
        "no_distractions": 5,
    }
    signals: List[Signal] = []
    findings: List[Finding] = []
    measured_w = 0
    earned = 0.0
    for name, w in weights.items():
        if name not in checks:
            signals.append(Signal(f"landing.{name}", None, w,
                                  skipped_reason="not provided: check not recorded"))
            continue
        val = 1.0 if checks.get(name) else 0.0
        pts = round(w * val, 1)
        signals.append(Signal(f"landing.{name}", pts, w))
        measured_w += w
        earned += pts
        if val == 0:
            findings.append(Finding(f"landing.{name}", 0, "medium", "low", w,
                                    f"Landing check failed: {name.replace('_', ' ')}",
                                    f"Recorded value for '{name}' is false/0."))
    composite = round(100.0 * earned / measured_w, 1) if measured_w else None
    for i, f in enumerate(sorted(findings, key=lambda f: -f.points_lost), start=1):
        f.priority = i
    return make_envelope(
        "audit", "landing-page",
        toolkit_version=TOOLKIT_VERSION, scoring_version=SCORING_VERSION, data_version=DATA_VERSION,
        evidence_stamp=CURRENT,
        missing=[s.id for s in signals if s.value is None],
        signal_count=sum(1 for s in signals if s.value is not None),
        signal_total=len(signals),
        scores={"composite": composite, "tier": tier_for(composite)},
        signals=signals, findings=findings,
        metrics={"score": composite, "checks_recorded": len(checks), "checks_total": len(weights)},
    )


def offer_math(*, price: float, discount_pct: Optional[float] = None,
               bundle_items: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """Offer economics: discounted price, savings, bundle value and effective per-unit price."""
    out: Dict[str, Any] = {"price": price}
    if discount_pct is not None:
        if discount_pct < 0 or discount_pct > 100:
            return {"error": "discount_pct must be 0..100"}
        disc_price = round(price * (1 - discount_pct / 100.0), 2)
        out["discount"] = {"pct": discount_pct, "discounted_price": disc_price,
                           "savings": round(price - disc_price, 2)}
    if bundle_items:
        total = sum((i.get("price") or 0) * (i.get("qty") or 1) for i in bundle_items)
        bundle_price = price
        out["bundle"] = {
            "items": bundle_items,
            "sum_of_parts": round(total, 2),
            "bundle_price": bundle_price,
            "savings": round(total - bundle_price, 2),
            "effective_discount_pct": round(100.0 * (total - bundle_price) / total, 2) if total else None,
        }
    return out
