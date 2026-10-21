"""``dconv`` — the deterministic command line for doddle-conversion-skills."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List, Optional

from . import DATA_VERSION, SCORING_VERSION, TOOLKIT_VERSION
from . import calc, frameworks as fw_mod
from .envelope import CURRENT, utc_now


def _emit(obj: Any, as_json: bool) -> None:
    if as_json:
        sys.stdout.write(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")
    else:
        sys.stdout.write(_human(obj) + "\n")


def _base(command: str, target: str) -> Dict[str, Any]:
    return {"ok": True, "command": command, "target": target, "generated_at": utc_now(),
            "toolkit_version": TOOLKIT_VERSION, "scoring_version": SCORING_VERSION,
            "data_version": DATA_VERSION, "evidence": {"stamp": CURRENT}}


def _human(obj: Dict[str, Any]) -> str:
    if obj.get("error"):
        e = obj["error"]
        return f"ERROR: {e.get('message')}\n  hint: {e.get('hint')}"
    cmd = obj.get("command")
    if cmd == "frameworks":
        rows = obj.get("frameworks") or []
        return "\n".join(f"{r['slug']}: {r['name']} — {r['purpose']}" for r in rows)
    if obj.get("metrics") and not isinstance(obj["metrics"].get("steps"), list):
        return f"{cmd} {obj.get('target')}: " + ", ".join(f"{k}={v}" for k, v in obj["metrics"].items() if not isinstance(v, (list, dict)))
    return json.dumps(obj, indent=2, ensure_ascii=False)


def _wants_json(args: argparse.Namespace) -> bool:
    return bool(getattr(args, "json", False)) or not sys.stdout.isatty()


def _num(v: Optional[str]) -> Optional[float]:
    if v in (None, ""):
        return None
    try:
        return float(str(v))
    except ValueError:
        return None


def cmd_version(args: argparse.Namespace) -> int:
    _emit({"toolkit": "doddle-conversion", "toolkit_version": TOOLKIT_VERSION,
           "scoring_version": SCORING_VERSION, "data_version": DATA_VERSION,
           "frameworks": fw_mod.slugs(), "python": sys.version.split()[0]}, True)
    return 0


def cmd_frameworks(args: argparse.Namespace) -> int:
    if args.name:
        fw = fw_mod.get(args.name)
        if fw is None:
            _emit({"ok": False, "command": "frameworks", "target": args.name, "error": {
                "message": f"unknown framework '{args.name}'",
                "hint": "Known: " + ", ".join(fw_mod.slugs())}}, _wants_json(args))
            return 1
        payload = dict(_base("frameworks", fw["slug"]), frameworks=[fw])
    else:
        payload = dict(_base("frameworks", "all"), frameworks=fw_mod.all_frameworks())
    _emit(payload, _wants_json(args))
    return 0


def cmd_ab_test(args: argparse.Namespace) -> int:
    res = calc.ab_test(args.control_n, args.control_conv, args.variant_n, args.variant_conv)
    if "error" in res:
        _emit({"ok": False, "command": "ab-test", "target": "ab-test", "error": {
            "message": res["error"], "hint": "Pass --control-n, --control-conv, --variant-n, --variant-conv."}}, _wants_json(args))
        return 1
    payload = _base("ab-test", "ab-test")
    payload["metrics"] = res
    _emit(payload, _wants_json(args))
    return 0


def cmd_sample_size(args: argparse.Namespace) -> int:
    res = calc.sample_size(baseline_rate=_num(args.baseline), mde=_num(args.mde),
                           alpha=_num(args.alpha) or 0.05, power=_num(args.power) or 0.8)
    if "error" in res:
        _emit({"ok": False, "command": "sample-size", "target": "sample-size", "error": {
            "message": res["error"], "hint": "baseline in (0,1), mde > 0."}}, _wants_json(args))
        return 1
    payload = _base("sample-size", "sample-size")
    payload["metrics"] = res
    _emit(payload, _wants_json(args))
    return 0


def cmd_funnel(args: argparse.Namespace) -> int:
    stages = []
    for spec in args.stage or []:
        name, _, count = spec.partition(":")
        stages.append({"name": name.strip(), "count": _num(count)})
    if len(stages) < 2:
        _emit({"ok": False, "command": "funnel", "target": "funnel", "error": {
            "message": "need at least two stages", "hint": "Pass --stage name:count at least twice"}}, _wants_json(args))
        return 1
    result = calc.funnel(stages)
    payload = _base("funnel", " -> ".join(s["name"] for s in stages))
    payload["metrics"] = {"overall_conversion": result["overall_conversion"], "steps": result["steps"]}
    _emit(payload, _wants_json(args))
    return 0


def cmd_landing_audit(args: argparse.Namespace) -> int:
    import json as _json
    checks = {}
    if args.checks:
        try:
            checks = _json.loads(args.checks)
        except Exception:  # noqa: BLE001
            _emit({"ok": False, "command": "landing-audit", "target": "landing", "error": {
                "message": "invalid --checks JSON", "hint": 'Pass a JSON object, e.g. {"clear_headline":true}'}}, _wants_json(args))
            return 1
    if args.file:
        with open(args.file, encoding="utf-8") as fh:
            checks = _json.load(fh)
    env = calc.landing_audit(checks)
    _emit(env, _wants_json(args))
    return 0 if env["ok"] else 1


def cmd_offer(args: argparse.Namespace) -> int:
    import json as _json
    bundle = None
    if args.bundle:
        try:
            bundle = _json.loads(args.bundle)
        except Exception:  # noqa: BLE001
            _emit({"ok": False, "command": "offer", "target": "offer", "error": {
                "message": "invalid --bundle JSON", "hint": 'Pass a JSON array of {"price","qty"}'}}, _wants_json(args))
            return 1
    res = calc.offer_math(price=_num(args.price), discount_pct=_num(args.discount),
                          bundle_items=bundle)
    if "error" in res:
        _emit({"ok": False, "command": "offer", "target": "offer", "error": {
            "message": res["error"], "hint": "price required; discount 0..100."}}, _wants_json(args))
        return 1
    payload = _base("offer", "offer")
    payload["metrics"] = res
    _emit(payload, _wants_json(args))
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    checks = [
        {"name": "python", "ok": sys.version_info >= (3, 9), "detail": sys.version.split()[0]},
        {"name": "toolkit_import", "ok": True, "detail": TOOLKIT_VERSION},
        {"name": "frameworks", "ok": len(fw_mod.slugs()) >= 1, "detail": f"{len(fw_mod.slugs())} registered"},
    ]
    ok = all(c["ok"] for c in checks)
    _emit({"ok": ok, "command": "doctor", "checks": checks}, True)
    return 0 if ok else 1


def build_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json", action="store_true", help="force JSON output")
    p = argparse.ArgumentParser(prog="dconv", description="Doddle Conversion deterministic toolkit")
    p.add_argument("--version", action="store_true", help="print versions")
    sub = p.add_subparsers(dest="subcommand")
    sp = sub.add_parser("version", help="print versions"); sp.add_argument("--json", action="store_true"); sp.set_defaults(func=cmd_version)
    sp = sub.add_parser("frameworks", parents=[common], help="the conversion framework registry")
    sp.add_argument("--name", help="one framework slug"); sp.set_defaults(func=cmd_frameworks)
    sp = sub.add_parser("ab-test", parents=[common], help="two-proportion z-test for A/B")
    sp.add_argument("--control-n", type=int, required=True, dest="control_n")
    sp.add_argument("--control-conv", type=int, required=True, dest="control_conv")
    sp.add_argument("--variant-n", type=int, required=True, dest="variant_n")
    sp.add_argument("--variant-conv", type=int, required=True, dest="variant_conv")
    sp.set_defaults(func=cmd_ab_test)
    sp = sub.add_parser("sample-size", parents=[common], help="required sample size per arm")
    sp.add_argument("--baseline", required=True); sp.add_argument("--mde", required=True)
    sp.add_argument("--alpha"); sp.add_argument("--power"); sp.set_defaults(func=cmd_sample_size)
    sp = sub.add_parser("funnel", parents=[common], help="conversion funnel")
    sp.add_argument("--stage", action="append", required=True); sp.set_defaults(func=cmd_funnel)
    sp = sub.add_parser("landing-audit", parents=[common], help="score a landing page")
    sp.add_argument("--checks"); sp.add_argument("--file"); sp.set_defaults(func=cmd_landing_audit)
    sp = sub.add_parser("offer", parents=[common], help="offer economics")
    sp.add_argument("--price", required=True); sp.add_argument("--discount"); sp.add_argument("--bundle")
    sp.set_defaults(func=cmd_offer)
    sp = sub.add_parser("doctor", help="check the environment")
    sp.add_argument("--json", action="store_true"); sp.set_defaults(func=cmd_doctor)
    return p


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if getattr(args, "version", False):
        return cmd_version(argparse.Namespace(subcommand="version", json=True))
    if not getattr(args, "func", None):
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
