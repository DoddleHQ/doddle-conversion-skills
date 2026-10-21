import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, ".claude", "skills")
AGENTS = os.path.join(ROOT, ".claude", "agents")
COMMON = os.path.join(SKILLS, "common")
TOOL_RE = re.compile(r"\bdoddle\.tool\.[A-Za-z0-9_.]+")
MARKET_RE = re.compile(r"\$\s?\d+(\.\d+)?\s?(B|M|bn|billion|million)\b", re.IGNORECASE)


def _read(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def test_thirty_skills():
    dirs = [d for d in os.listdir(SKILLS) if os.path.isdir(os.path.join(SKILLS, d)) and d != "common"]
    assert len(dirs) == 30


def test_skill_structure():
    for d in os.listdir(SKILLS):
        if d == "common" or not os.path.isdir(os.path.join(SKILLS, d)):
            continue
        base = os.path.join(SKILLS, d)
        assert os.path.isfile(os.path.join(base, "SKILL.md"))
        assert os.path.isfile(os.path.join(base, "blueprint.yaml"))
        text = _read(os.path.join(base, "SKILL.md"))
        assert "id: doddle.conv." + d in text
        bp = _read(os.path.join(base, "blueprint.yaml"))
        assert "id: doddle.conv." + d in bp
        for tool in set(TOOL_RE.findall(bp)):
            assert tool in {"doddle.tool.cli.dconv", "doddle.tool.v1.ga4.getReport",
                            "doddle.tool.v1.hubspot.contacts", "doddle.tool.v1.clearbit.company",
                            "doddle.tool.v1.notion.pages", "doddle.tool.v1.canva.design"}, tool
        for fname in ("SKILL.md", "blueprint.yaml"):
            assert not MARKET_RE.search(_read(os.path.join(base, fname)))


def test_common_refs_present():
    for ref in ("response-contract.md", "data-reliability.md", "fundamentals.md",
                "scoring-methodology.md", "frameworks-registry.md", "mcp-integration-guide.md"):
        assert os.path.isfile(os.path.join(COMMON, ref))


def test_five_agents():
    agents = sorted(f for f in os.listdir(AGENTS) if f.endswith(".md"))
    assert agents == ["conversion-strategist.md", "cro-analyst.md", "experiment-lead.md",
                      "offer-strategist.md", "ux-researcher.md"]


def test_manifests_parse():
    for rel in (".claude-plugin/plugin.json", "marketplace.json", "package.json"):
        json.loads(_read(os.path.join(ROOT, rel)))
