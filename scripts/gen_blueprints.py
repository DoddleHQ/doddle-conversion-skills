from __future__ import annotations
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, ".claude", "skills")

SPECS = [
    ("conv-strategy", "conversion-strategist", "toolkit", ["landing-audit"], [], [("goal","string",True,"Conversion goal"),("metric","string",False,"Primary metric")], [("plan","markdown","Conversion program plan")], []),
    ("cro-audit", "cro-analyst", "toolkit", ["landing-audit"], ["ga4.getReport"], [("page","string",True,"Page or flow to audit"),("checks","string",False,"Recorded check results JSON")], [("report","markdown","CRO audit report"),("envelope","json","Audit envelope")], ["ga4"]),
    ("cro-research", "ux-researcher", "advisory", [], [], [("page","string",True,"Page or flow"),("evidence","file",False,"User research notes")], [("research","markdown","Research findings")], []),
    ("cro-heuristics", "ux-researcher", "toolkit", [], [], [("page","string",True,"Page to review")], [("review","markdown","LIFT heuristic review")], []),
    ("cro-copy", "conversion-strategist", "advisory", [], ["canva.design"], [("page","string",True,"Page"),("offer","string",False,"Offer")], [("copy","markdown","Conversion copy")], ["canva"]),
    ("cro-ux", "ux-researcher", "toolkit", ["landing-audit"], [], [("page","string",True,"Page")], [("review","markdown","UX friction review"),("envelope","json","Audit envelope")], []),
    ("conv-landing-page", "conversion-strategist", "toolkit", [], ["canva.design"], [("offer","string",True,"Offer"),("audience","string",False,"Audience")], [("page","markdown","Landing page")], ["canva"]),
    ("conv-landing-audit", "cro-analyst", "toolkit", ["landing-audit"], ["ga4.getReport"], [("checks","string",True,"Recorded checks JSON"),("page","string",False,"Page name")], [("report","markdown","Landing audit report"),("envelope","json","Audit envelope")], ["ga4"]),
    ("cro-forms", "ux-researcher", "toolkit", [], [], [("form","string",True,"Form to optimize")], [("plan","markdown","Form optimization plan")], []),
    ("cro-mobile", "ux-researcher", "toolkit", [], [], [("page","string",True,"Page")], [("plan","markdown","Mobile conversion plan")], []),
    ("cro-speed", "cro-analyst", "advisory", [], ["ga4.getReport"], [("page","string",True,"Page")], [("report","markdown","Speed report")], ["ga4"]),
    ("cro-trust", "ux-researcher", "toolkit", [], [], [("page","string",True,"Page")], [("plan","markdown","Trust signals plan")], []),
    ("conv-offer-design", "offer-strategist", "toolkit", [], [], [("value","string",True,"Core value"),("price","number",False,"Price")], [("offer","markdown","Offer design")], []),
    ("conv-pricing-page", "offer-strategist", "toolkit", [], [], [("tiers","string",True,"Tiers")], [("page","markdown","Pricing page")], []),
    ("conv-discount-strategy", "offer-strategist", "toolkit", ["offer"], [], [("price","number",True,"List price"),("discount","number",False,"Discount pct")], [("analysis","markdown","Discount analysis"),("envelope","json","Offer envelope")], []),
    ("conv-bundle-design", "offer-strategist", "toolkit", ["offer"], [], [("price","number",True,"Bundle price"),("bundle","string",True,"Items JSON")], [("analysis","markdown","Bundle analysis"),("envelope","json","Offer envelope")], []),
    ("conv-guarantee", "offer-strategist", "advisory", [], [], [("offer","string",True,"Offer")], [("copy","markdown","Guarantee copy")], []),
    ("conv-experiment-design", "experiment-lead", "toolkit", [], ["notion.pages"], [("hypothesis","string",True,"Hypothesis"),("metric","string",True,"Primary metric")], [("brief","markdown","Experiment brief")], ["notion"]),
    ("conv-ab-testing", "experiment-lead", "toolkit", ["ab-test"], [], [("control_n","number",True,"Control visitors"),("control_conv","number",True,"Control conversions"),("variant_n","number",True,"Variant visitors"),("variant_conv","number",True,"Variant conversions")], [("result","markdown","A/B result"),("envelope","json","AB envelope")], []),
    ("conv-multivariate", "experiment-lead", "toolkit", [], [], [("variants","string",True,"Variants")], [("plan","markdown","MVT plan")], []),
    ("conv-hypothesis", "experiment-lead", "advisory", [], [], [("observation","string",True,"Observation")], [("hypothesis","markdown","Hypothesis")], []),
    ("conv-significance", "experiment-lead", "toolkit", ["ab-test"], [], [("control_n","number",True,"Control visitors"),("control_conv","number",True,"Control conversions"),("variant_n","number",True,"Variant visitors"),("variant_conv","number",True,"Variant conversions")], [("result","markdown","Significance result"),("envelope","json","AB envelope")], []),
    ("conv-experiment-reporting", "experiment-lead", "toolkit", ["ab-test"], [], [("control_n","number",True,"Control visitors"),("control_conv","number",True,"Control conversions"),("variant_n","number",True,"Variant visitors"),("variant_conv","number",True,"Variant conversions")], [("report","markdown","Experiment report"),("envelope","json","AB envelope")], []),
    ("conv-personalization", "conversion-strategist", "toolkit", [], ["hubspot.contacts","clearbit.company"], [("segments","string",True,"Segments")], [("plan","markdown","Personalization plan")], ["hubspot","clearbit"]),
    ("conv-segmentation", "conversion-strategist", "advisory", [], ["hubspot.contacts"], [("data","string",True,"Segment data")], [("segments","markdown","Conversion segments")], ["hubspot"]),
    ("conv-dynamic-content", "conversion-strategist", "advisory", [], ["canva.design"], [("page","string",True,"Page")], [("plan","markdown","Dynamic content plan")], ["canva"]),
    ("conv-geo-targeting", "conversion-strategist", "advisory", [], [], [("markets","string",True,"Markets")], [("plan","markdown","Geo targeting plan")], []),
    ("conv-metrics", "cro-analyst", "toolkit", ["landing-audit"], ["ga4.getReport"], [("checks","string",False,"Checks JSON"),("window","string",False,"Window")], [("scorecard","markdown","Conversion scorecard"),("envelope","json","Audit envelope")], ["ga4"]),
    ("conv-funnel", "cro-analyst", "toolkit", ["funnel"], ["ga4.getReport"], [("stages","string",True,"Stage counts")], [("analysis","markdown","Funnel analysis"),("envelope","json","Funnel envelope")], ["ga4"]),
    ("conv-attribution", "cro-analyst", "advisory", [], ["ga4.getReport"], [("window","string",True,"Window")], [("report","markdown","Attribution report")], ["ga4"]),
]

INTEGRATION_TOOL = {
    "ga4": "doddle.tool.v1.ga4.getReport",
    "hubspot": "doddle.tool.v1.hubspot.contacts",
    "clearbit": "doddle.tool.v1.clearbit.company",
    "notion": "doddle.tool.v1.notion.pages",
    "canva": "doddle.tool.v1.canva.design",
}


def _inputs_yaml(inputs):
    out = ["inputs:"]
    for name, typ, req, desc in inputs:
        out.append(f'  - {{name: {name}, type: {typ}, required: {str(req).lower()}, description: "{desc}"}}')
    return out


def _outputs_yaml(outputs):
    out = ["outputs:"]
    for name, typ, desc in outputs:
        out.append(f'  - {{name: {name}, type: {typ}, description: "{desc}"}}')
    return out


def build(spec):
    slug, agent, kind, commands, mcp, inputs, outputs, integrations = spec
    if kind == "toolkit" and not commands:
        commands = ["frameworks"]
    sid = f"doddle.conv.{slug}"
    tools = ["tools:", "  - {id: doddle.tool.cli.dconv, required: false, fallback: manual_review}"]
    for m in mcp:
        tools.append(f"  - {{id: doddle.tool.v1.{m}, required: false, fallback: manual_review}}")
    md_out = next((o[0] for o in outputs if o[1] == "markdown"), "report")
    env_out = next((o[0] for o in outputs if o[1] == "json"), "envelope")
    lines = [f"id: {sid}", "version: 0.1.0", "kind: skill", "engine: doddle-os>=1.0",
             f'description: "{agent} skill for {slug.replace("conv-","").replace("cro-","").replace("-"," ")}."',
             *_inputs_yaml(inputs), *_outputs_yaml(outputs), *tools]
    if integrations:
        lines.append("integrations:")
        for i in integrations:
            lines.append(f"  - {i}")
    lines.append("nodes:")
    if kind == "toolkit":
        node_ids = []
        for i, cmd in enumerate(commands):
            nid = "run" if i == 0 else f"run_{i+1}"
            node_ids.append(nid)
            lines.append(f'  - {{id: {nid}, type: tool, ref: doddle.tool.cli.dconv, args: ["{cmd}"], needs: [{"inputs" if i == 0 else node_ids[i-1]}], produces: [{env_out}]}}')
        last = node_ids[-1]
        lines.append(f'  - {{id: narrate, type: agent, ref: {agent}, needs: [{last}], produces: [{md_out}]}}')
    else:
        lines.append(f'  - {{id: analyze, type: agent, ref: {agent}, needs: [inputs], produces: [{md_out}]}}')
    lines.append("on_fail: {retry: 1, fallback: manual_review}")
    return "\n".join(lines) + "\n"


def main():
    for spec in SPECS:
        slug = spec[0]
        d = os.path.join(SKILLS, slug)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "blueprint.yaml"), "w", encoding="utf-8") as fh:
            fh.write(build(spec))
    print(f"wrote {len(SPECS)} blueprints")


if __name__ == "__main__":
    main()
