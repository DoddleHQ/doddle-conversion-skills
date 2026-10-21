"""The conversion framework registry — named CRO templates, versioned as one unit."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

FRAMEWORKS: Dict[str, Dict[str, Any]] = {
    "landing-page-anatomy": {
        "name": "Landing Page Anatomy",
        "purpose": "Structure a high-converting landing page.",
        "sections": ["Above-the-fold promise", "Headline + subhead", "Primary CTA", "Proof (social proof, logos, testimonials)",
                     "Benefits (3)", "How it works", "Objection handling", "Secondary CTA", "Footer / legal"],
    },
    "ab-test-brief": {
        "name": "A/B Test Brief",
        "purpose": "Design a test before it runs.",
        "sections": ["Hypothesis", "Primary metric", "Guardrail metrics", "Variants", "Population & split",
                     "Sample size & duration", "Decision rule", "Rollback plan"],
    },
    "cro-heuristics": {
        "name": "CRO Heuristics (LIFT)",
        "purpose": "Diagnose a page with the LIFT model.",
        "sections": ["Value proposition", "Relevance", "Clarity", "Urgency", "Anxiety (trust)", "Distraction"],
    },
    "offer-design": {
        "name": "Offer Design",
        "purpose": "Design an offer that converts.",
        "sections": ["Core value", "Price & value metric", "Bonuses", "Guarantee", "Scarcity/urgency (honest)",
                     "Risk reversal", "CTA"],
    },
    "form-optimization": {
        "name": "Form Optimization",
        "purpose": "Reduce friction in a form.",
        "sections": ["Fields (must-have vs nice-to-have)", "Field order", "Labels & placeholders",
                     "Validation & errors", "Progressive profiling", "Mobile input types", "Submit button copy"],
    },
    "pricing-page": {
        "name": "Pricing Page",
        "purpose": "Structure a pricing page.",
        "sections": ["Tier names", "Value metric", "Feature matrix", "Recommended tier", "FAQ", "Social proof",
                     "Annual/monthly toggle", "Enterprise CTA"],
    },
    "personalization": {
        "name": "Personalization Plan",
        "purpose": "Plan 1:1 or segment-level personalization.",
        "sections": ["Segments", "Signals available", "Variants per segment", "Fallback", "Measurement",
                     "Privacy/consent"],
    },
    "experimentation-program": {
        "name": "Experimentation Program",
        "purpose": "Run experimentation as a program, not one-offs.",
        "sections": ["Hypothesis backlog", "Prioritization (ICE/RICE)", "Test cadence", "Guardrails",
                     "Documentation", "Learning log", "Rollout policy"],
    },
    "trust-signals": {
        "name": "Trust Signals",
        "purpose": "Catalog trust elements for a page.",
        "sections": ["Security badges", "Social proof", "Guarantees", "Transparency (pricing, terms)",
                     "Third-party validation", "Contact & support"],
    },
    "mobile-conversion": {
        "name": "Mobile Conversion",
        "purpose": "Optimize conversion on mobile.",
        "sections": ["Thumb-zone CTAs", "Form input types", "Page weight", "Sticky CTA", "Tap targets",
                     "Mobile-specific copy"],
    },
    "funnel-diagnosis": {
        "name": "Funnel Diagnosis",
        "purpose": "Diagnose a conversion funnel.",
        "sections": ["Stage definitions", "Drop-off by stage", "Segment breakdown", "Hypotheses",
                     "Quick wins", "Measurement gaps"],
    },
    "cro-audit": {
        "name": "CRO Audit",
        "purpose": "Full conversion audit of a page or flow.",
        "sections": ["Objective & primary metric", "Heuristic review (LIFT)", "Analytics review",
                     "User research", "Technical (speed, mobile)", "Prioritized experiments", "Quick wins"],
    },
}

REGISTRY_VERSION = "conversion-frameworks-2026-10"


def get(slug: str) -> Optional[Dict[str, Any]]:
    if not slug:
        return None
    key = slug.strip().lower()
    fw = FRAMEWORKS.get(key)
    return dict(fw, slug=key) if fw else None


def all_frameworks() -> List[Dict[str, Any]]:
    return [dict(fw, slug=slug) for slug, fw in sorted(FRAMEWORKS.items())]


def slugs() -> List[str]:
    return sorted(FRAMEWORKS)
