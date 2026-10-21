"""Toolkit tests for dconv."""

import json
import os
import subprocess
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from doddle_conversion import calc  # noqa: E402

CLI = os.path.join(ROOT, "scripts", "dconv")


def test_ab_test():
    r = calc.ab_test(1000, 50, 1000, 75)
    assert r["winner"] == "variant"
    assert r["significant_at_95"] is True
    assert r["lift_relative"] == 0.5


def test_ab_test_inconclusive():
    r = calc.ab_test(100, 5, 100, 6)
    assert r["winner"] == "inconclusive"


def test_sample_size():
    r = calc.sample_size(baseline_rate=0.05, mde=0.02)
    assert r["per_arm"] > 0
    assert r["total"] == r["per_arm"] * 2


def test_landing_audit():
    r = calc.landing_audit({"clear_headline": True, "single_cta": False})
    assert r["scores"]["composite"] is not None
    assert r["scores"]["tier"] in ("Excellent", "Good", "Fair", "Weak", "Critical")


def test_offer():
    r = calc.offer_math(price=99, discount_pct=20)
    assert r["discount"]["discounted_price"] == 79.2


def test_funnel():
    r = calc.funnel([{"name": "v", "count": 1000}, {"name": "c", "count": 50}])
    assert r["steps"][0]["conversion"] == 0.05


@pytest.mark.parametrize("args,expect", [
    (["version"], "toolkit_version"),
    (["doctor"], "checks"),
    (["ab-test", "--control-n", "1000", "--control-conv", "50", "--variant-n", "1000", "--variant-conv", "75"], "metrics"),
    (["sample-size", "--baseline", "0.05", "--mde", "0.02"], "metrics"),
    (["landing-audit", "--checks", '{"clear_headline":true}'], "scores"),
])
def test_cli_commands(args, expect):
    out = subprocess.run([sys.executable, CLI, *args], capture_output=True, text=True)
    assert out.returncode == 0, out.stderr
    payload = json.loads(out.stdout)
    assert expect in payload
