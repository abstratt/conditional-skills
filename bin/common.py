import json, os, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
RUNS = RESULTS / "runs"

SUBJECTS = {
    "claude-opus":   {"harness": "claude-code", "model": "claude-opus-5"},
    "claude-sonnet": {"harness": "claude-code", "model": "claude-sonnet-5"},
    "claude-haiku":  {"harness": "claude-code", "model": "claude-haiku-4-5-20251001"},
    "codex-default": {"harness": "codex",       "model": "gpt-5.6-luna"},
}
DELIVERIES = ["native", "pointer", "inline"]


def load_prompts(study=None):
    out = []
    for f in ("branch.jsonl", "work.jsonl", "gate.jsonl"):
        for line in (ROOT / "prompts" / f).read_text().splitlines():
            if line.strip():
                p = json.loads(line)
                if study in (None, p["study"]):
                    out.append(p)
    return out


def prompt_skills(p):
    """The skills a prompt installs: one for most prompts, a set for Study 3's selection prompts, none for baselines."""
    if p.get("skills"):
        return list(p["skills"])
    return [p["skill"]] if p.get("skill") else []


def skill_frontmatter(name):
    text = (ROOT / "skills" / name / "SKILL.md").read_text()
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    fm = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        fm[k.strip()] = v.strip()
    return fm, text


def ground_truth():
    return json.loads((ROOT / "ground_truth.json").read_text())


def run_dirs():
    return sorted(d for d in RUNS.iterdir() if (d / "meta.json").exists()) if RUNS.exists() else []


def read_json(p, default=None):
    try:
        return json.loads(Path(p).read_text())
    except Exception:
        return default
