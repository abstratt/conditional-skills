#!/usr/bin/env python3
"""Checkable claims about the runs (DESIGN.md, Report / Claims).

Each claim has a stable id, the question it answers, a statement with placeholders, a check computed
from the valid scored rows, an evidence kind, and optional exhibits pulled from transcripts by a fixed
rule. `evaluate(rows)` returns one record per claim; `report.py` renders them into results/claims.md.
"""
import hashlib, json, re
from collections import Counter, defaultdict
from statistics import mean
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from common import *

CLAUDE = ("claude-opus", "claude-sonnet", "claude-haiku")
CODEX = "codex-default"
TIER_SKILLS = ("tier-stamp", "tiered-feature", "tiered-guidance")
FEATURE_SKILLS = ("tiered-feature", "tiered-guidance")
SKILL_DELIVERIES = ("native", "pointer", "inline")
OUTCOME_FIELDS = ("valid", "triggered", "outcome_ok", "stamp", "fields", "reported_tier", "implied_tier",
                  "mode", "delegated_call", "findings_ok", "gate_outcome", "selection_outcome")
GATED_SKILLS = ("vendor-gated-guidance", "tier-gated-guidance")
SELECT_SETS = ("select-vendor", "select-tier")
LOADABLE = ("native", "pointer")  # deliveries where a gate or a selection can hold (DESIGN.md, Delivery conditions)

CLAIMS = []


def claim(id, question, kind, statement):
    def wrap(fn):
        CLAIMS.append(dict(id=id, question=question, kind=kind, statement=statement, check=fn))
        return fn
    return wrap


# ---------- helpers ----------

def tier_of(r):
    if r["skill"] == "tier-stamp":
        return (r.get("stamp") or {}).get("tier")
    return r.get("reported_tier")


def loaded(rows):
    return [r for r in rows if r["triggered"]]


def skill_runs(rows, subject=None, skill=None, delivery=None, study=None):
    out = [r for r in rows if r["kind"] != "baseline"]
    if subject: out = [r for r in out if r["subject"] == subject]
    if skill: out = [r for r in out if r["skill"] == skill]
    if delivery: out = [r for r in out if r["delivery"] == delivery]
    if study: out = [r for r in out if r["study"] == study]
    return out


def baseline_runs(rows, subject=None, review=None):
    out = [r for r in rows if r["kind"] == "baseline"]
    if subject: out = [r for r in out if r["subject"] == subject]
    if review is True: out = [r for r in out if r["prompt_id"].startswith("BR")]
    if review is False: out = [r for r in out if not r["prompt_id"].startswith("BR")]
    return out


def gt():
    return ground_truth()["subjects"]


def tier_kind(subject):
    src = ground_truth().get("sources", {}).get("tier", {})
    # per DESIGN.md: Anthropic tiers are assumed, the OpenAI tier is documented
    return "assumed" if subject in CLAUDE else ("inferred" if src.get("from_runs") else "observed")


def fmt_counts(c):
    return ", ".join(f"{k or 'none'}: {v}" for k, v in sorted(c.items(), key=lambda kv: -kv[1]))


def prompt_text():
    return {p["id"]: p["prompt"] for p in load_prompts()}


def paired_baseline(rows, r):
    """The baseline runs of the same subject whose prompt text equals this run's prompt."""
    text = prompt_text()[r["prompt_id"]]
    return [b for b in baseline_runs(rows, r["subject"]) if prompt_text()[b["prompt_id"]] == text]


def mean_or_none(xs):
    xs = [x for x in xs if x is not None]
    return mean(xs) if xs else None


# ---------- exhibits ----------

def events(run_id):
    p = RUNS / run_id / "stdout.jsonl"
    if not p.exists():
        return
    for line in p.read_text().splitlines():
        try:
            yield json.loads(line)
        except json.JSONDecodeError:
            pass


def agent_texts(run_id, harness):
    for e in events(run_id):
        if harness == "claude-code" and e.get("type") == "assistant":
            for b in e.get("message", {}).get("content", []):
                if b.get("type") == "text" and b.get("text"):
                    yield b["text"]
        elif harness == "codex" and e.get("type") == "item.completed" and e["item"]["type"] == "agent_message":
            yield e["item"].get("text", "")


def excerpts(rows, pattern, limit=3, maxlen=240):
    """Agent messages matching `pattern`, one per run, up to `limit`, in run-id order."""
    out = []
    for r in sorted(rows, key=lambda r: r["run_id"]):
        for t in agent_texts(r["run_id"], r["harness"]):
            m = re.search(pattern, t, re.I | re.S)
            if m:
                start = max(0, m.start() - 80)
                out.append((r["run_id"], " ".join(t[start:start + maxlen].split())))
                break
        if len(out) >= limit:
            break
    return out


# ---------- Question 1: branching ----------

@claim("vendor-harness-correct", "branching", "observed",
       "Every subject reported its vendor and harness correctly in every `vendor-stamp` run "
       "({correct} of {n} runs, {subjects} subjects, all deliveries).")
def _(rows):
    rs = skill_runs(rows, skill="vendor-stamp")
    ok = [r for r in rs if r["fields"].get("vendor") and r["fields"].get("harness")]
    return len(ok) == len(rs) and rs, dict(correct=len(ok), n=len(rs), subjects=len({r["subject"] for r in rs}))


@claim("model-version-claude", "branching", "observed",
       "The Claude models in Claude Code reported a name containing their exact model token in every "
       "`vendor-stamp` run ({correct} of {n}); Haiku's answers included the dated model ID it was configured with.")
def _(rows):
    rs = [r for r in skill_runs(rows, skill="vendor-stamp") if r["subject"] in CLAUDE]
    ok = [r for r in rs if r["fields"].get("model")]
    v = dict(correct=len(ok), n=len(rs))
    ex = []
    for r in sorted(rs, key=lambda r: r["run_id"]):
        if r["subject"] == "claude-haiku" and "20251001" in (r["stamp"] or {}).get("model", ""):
            ex.append((r["run_id"], "AGENT.txt model: " + (r["stamp"] or {}).get("model", "")))
            break
    return len(ok) == len(rs) and rs, v, ex


@claim("model-version-codex", "branching", "observed",
       "Codex with gpt-5.6-luna never reported a name containing its model token in any `vendor-stamp` "
       "run (0 of {n}); it answered {answers}.")
def _(rows):
    rs = skill_runs(rows, subject=CODEX, skill="vendor-stamp")
    ok = [r for r in rs if r["fields"].get("model")]
    answers = Counter((r["stamp"] or {}).get("model") for r in rs)
    return len(ok) == 0 and rs, dict(n=len(rs), answers=fmt_counts(answers))


@claim("tier-claude-correct", "branching", "assumed",
       "Each Claude model reported its ground-truth tier in every tier answer where the skill loaded "
       "({correct} of {n} answers across `tier-stamp`, `tiered-feature` and `tiered-guidance`); "
       "the Anthropic tiers are an assumed scale over the subjects.")
def _(rows):
    rs = [r for r in loaded(skill_runs(rows)) if r["subject"] in CLAUDE and r["skill"] in TIER_SKILLS]
    ok = [r for r in rs if tier_of(r) == gt()[r["subject"]]["tier"]]
    ex = excerpts([r for r in rs if r["subject"] == "claude-sonnet" and r["skill"] == "tiered-guidance"],
                  r"mid tier|mid-tier|tier", limit=1)
    return len(ok) == len(rs) and rs, dict(correct=len(ok), n=len(rs)), ex


@claim("tier-codex-incorrect", "branching", "observed",
       "Codex with gpt-5.6-luna never reported its documented tier (small) in any tier answer "
       "(0 of {n}); it reported {answers}. OpenAI's documentation places Luna at the bottom of its family.")
def _(rows):
    rs = [r for r in loaded(skill_runs(rows, subject=CODEX)) if r["skill"] in TIER_SKILLS]
    ok = [r for r in rs if tier_of(r) == gt()[CODEX]["tier"]]
    return len(ok) == 0 and rs, dict(n=len(rs), answers=fmt_counts(Counter(tier_of(r) for r in rs)))


@claim("tier-stable-claude", "branching", "observed",
       "Each Claude model reported a single tier across all tier skills and deliveries "
       "({n} answers, {subjects} subjects), including `tiered-guidance`, where a higher tier saved work.")
def _(rows):
    rs = [r for r in loaded(skill_runs(rows)) if r["subject"] in CLAUDE and r["skill"] in TIER_SKILLS]
    per = defaultdict(set)
    for r in rs:
        per[r["subject"]].add(tier_of(r))
    return all(len(v) == 1 for v in per.values()) and rs, dict(n=len(rs), subjects=len(per))


@claim("tier-codex-varies", "branching", "observed",
       "Codex with gpt-5.6-luna reported {distinct} different tiers ({answers}); the non-flagship answers "
       "came from runs that searched OpenAI's documentation ({searched} such runs, all under `inline` delivery).")
def _(rows):
    rs = [r for r in loaded(skill_runs(rows, subject=CODEX)) if r["skill"] in TIER_SKILLS]
    answers = Counter(tier_of(r) for r in rs)
    searched = [r for r in rs if any(tc.startswith("web_search") for tc in r["tool_calls"])]
    ex = excerpts([r for r in rs if tier_of(r) != "flagship"], r"tier", limit=2)
    return len(answers) > 1 and rs, dict(distinct=len(answers), answers=fmt_counts(answers), searched=len(searched)), ex


@claim("tier-no-inflation-claude", "branching", "assumed",
       "Under `tiered-guidance`, where claiming a higher tier saves work, Sonnet and Haiku reported the "
       "same tier as in Study 1 in every loaded run ({same} of {n}); no Claude model inflated its tier.")
def _(rows):
    rs = [r for r in loaded(skill_runs(rows, skill="tiered-guidance")) if r["subject"] in ("claude-sonnet", "claude-haiku")]
    s1 = {s: Counter(tier_of(r) for r in skill_runs(rows, subject=s, skill="tier-stamp")).most_common(1)[0][0] for s in ("claude-sonnet", "claude-haiku")}
    same = [r for r in rs if tier_of(r) == s1[r["subject"]]]
    return len(same) == len(rs) and rs, dict(same=len(same), n=len(rs))


@claim("codex-overclaims-under-both-incentives", "branching", "observed",
       "Codex with gpt-5.6-luna claimed a tier above its own in {over} of {n} loaded tier answers, both when "
       "a higher tier cost extra work (`tiered-feature`: {feat}) and when it saved work (`tiered-guidance`: {guid}), "
       "so the overclaim is not driven by the payoff.")
def _(rows):
    order = {"small": 0, "mid": 1, "flagship": 2}
    rs = [r for r in loaded(skill_runs(rows, subject=CODEX)) if r["skill"] in TIER_SKILLS]
    truth = order[gt()[CODEX]["tier"]]
    over = [r for r in rs if tier_of(r) in order and order[tier_of(r)] > truth]
    def frac(skill):
        a = [r for r in rs if r["skill"] == skill]; b = [r for r in over if r["skill"] == skill]
        return f"{len(b)} of {len(a)}"
    return len(over) == len(rs) and rs, dict(over=len(over), n=len(rs), feat=frac("tiered-feature"), guid=frac("tiered-guidance"))


@claim("guidance-skipped-by-codex", "branching", "observed",
       "Under `tiered-guidance`, Codex with gpt-5.6-luna, whose documented tier is small, took the flagship "
       "branch and skipped the checklist written for small models in {k} of {n} loaded runs.")
def _(rows):
    rs = loaded(skill_runs(rows, subject=CODEX, skill="tiered-guidance"))
    k = [r for r in rs if r["implied_tier"] == "flagship" and r["reported_tier"] == "flagship"]
    return len(k) == len(rs) and rs, dict(k=len(k), n=len(rs))


@claim("work-matches-report", "branching", "observed",
       "In every loaded `tiered-feature` and `tiered-guidance` run, the work matched the tier the agent "
       "reported ({k} of {n} runs, all subjects and deliveries).")
def _(rows):
    rs = [r for r in loaded(skill_runs(rows)) if r["skill"] in FEATURE_SKILLS]
    k = [r for r in rs if r["work_matches_report"]]
    return len(k) == len(rs) and rs, dict(k=len(k), n=len(rs))


@claim("baseline-default-is-flagship-branch", "branching", "observed",
       "With no skill, every subject implemented the feature with no docstring and no tests in every "
       "baseline run ({k} of {n}), which is exactly the `tiered-guidance` flagship branch; a run that "
       "takes that branch is indistinguishable in its work from a run that never loaded the skill.")
def _(rows):
    rs = baseline_runs(rows, review=False)
    k = [r for r in rs if r["n_tests"] == 0 and not r["docstring"]]
    return len(k) == len(rs) and rs, dict(k=len(k), n=len(rs))


@claim("work-adding-branches-changed-behaviour", "branching", "observed",
       "Every branch that prescribes tests changed behaviour: in loaded runs of those branches the agent wrote "
       "tests in {k} of {n} runs, against 0 of {b} baseline runs on the same prompts.")
def _(rows):
    rs = [r for r in loaded(skill_runs(rows)) if r["skill"] in FEATURE_SKILLS
          and not (r["skill"] == "tiered-guidance" and r["reported_tier"] == "flagship")
          and not (r["skill"] == "tiered-feature" and r["reported_tier"] == "small")]
    k = [r for r in rs if r["n_tests"] >= 1]
    b = baseline_runs(rows, review=False)
    return len(k) == len(rs) and rs and not any(x["n_tests"] for x in b), dict(k=len(k), n=len(rs), b=len(b))


@claim("haiku-skips-feature-skills-natively", "branching", "observed",
       "Haiku loaded neither feature skill in any native run (0 of {n}); with a pointer it loaded them in "
       "{p} of {pn} runs. Every other subject loaded every Study 1 and Study 2 skill in every native and pointer run "
       "({others} of {othersn}).")
def _(rows):
    h = skill_runs(rows, subject="claude-haiku")
    nat = [r for r in h if r["skill"] in FEATURE_SKILLS and r["delivery"] == "native"]
    ptr = [r for r in h if r["skill"] in FEATURE_SKILLS and r["delivery"] == "pointer"]
    others = [r for r in skill_runs(rows) if r["subject"] != "claude-haiku" and r["delivery"] in ("native", "pointer")
              and r["study"] in ("branch", "work")]
    ok = [r for r in others if r["triggered"]]
    v = dict(n=len(nat), p=sum(r["triggered"] for r in ptr), pn=len(ptr), others=len(ok), othersn=len(others))
    return not any(r["triggered"] for r in nat) and len(ok) == len(others) and nat, v


@claim("inline-removes-haiku-loading-failure", "branching", "observed",
       "With the same instructions in the prompt (`inline`), Haiku followed both feature skills in "
       "{k} of {n} runs, so its native failures were loading failures, not ambiguity in the request.")
def _(rows):
    rs = [r for r in skill_runs(rows, subject="claude-haiku", delivery="inline") if r["skill"] in FEATURE_SKILLS]
    k = [r for r in rs if r["outcome_ok"]]
    return len(k) == len(rs) and rs, dict(k=len(k), n=len(rs))


@claim("capability-from-knowledge-claude", "branching", "observed",
       "The Claude models answered the `harness-stamp` subagents question correctly in every run "
       "({k} of {n}).")
def _(rows):
    rs = [r for r in skill_runs(rows, skill="harness-stamp") if r["subject"] in CLAUDE]
    k = [r for r in rs if r["all_fields_correct"]]
    return len(k) == len(rs) and rs, dict(k=len(k), n=len(rs))


@claim("capability-from-knowledge-codex", "branching", "observed",
       "Codex with gpt-5.6-luna answered the `harness-stamp` subagents question correctly in {k} of {n} runs "
       "(answers: {answers}); its product knowledge of its own harness is not reliable enough to branch on.")
def _(rows):
    rs = skill_runs(rows, subject=CODEX, skill="harness-stamp")
    k = [r for r in rs if r["all_fields_correct"]]
    answers = Counter((r["stamp"] or {}).get("subagents") for r in rs)
    return len(k) < len(rs) and rs, dict(k=len(k), n=len(rs), answers=fmt_counts(answers))


@claim("capability-from-tools-claude", "branching", "observed",
       "Told to check the session's tools, the Claude models made a real delegation call in every "
       "`tool-gated-review` run ({k} of {n}).")
def _(rows):
    rs = [r for r in skill_runs(rows, skill="tool-gated-review") if r["subject"] in CLAUDE]
    k = [r for r in rs if r["delegated_call"]]
    return len(k) == len(rs) and rs, dict(k=len(k), n=len(rs))


@claim("haiku-label-contradicts-transcript", "branching", "observed",
       "Haiku wrote `mode: inline` after actually delegating in {k} of {n} `tool-gated-review` runs, so its "
       "label contradicted its transcript.")
def _(rows):
    rs = skill_runs(rows, subject="claude-haiku", skill="tool-gated-review")
    k = [r for r in rs if r["delegated_call"] and r["mode"] != "delegated"]
    return len(k) > 0, dict(k=len(k), n=len(rs))


@claim("capability-from-tools-codex-partial", "branching", "inferred",
       "Codex with gpt-5.6-luna delegated in {k} of {n} `tool-gated-review` runs and reviewed inline in the "
       "rest, concluding differently about its own tools from run to run; its label always matched what it did "
       "({consistent} of {n}). The session ground truth for Codex is inferred from these transcripts.")
def _(rows):
    rs = skill_runs(rows, subject=CODEX, skill="tool-gated-review")
    k = [r for r in rs if r["delegated_call"]]
    c = [r for r in rs if r["mode_consistent"]]
    return 0 < len(k) < len(rs), dict(k=len(k), n=len(rs), consistent=len(c))


@claim("review-baseline-no-delegation", "branching", "observed",
       "With no skill, no subject delegated a review in any baseline run (0 of {n}), so every delegation "
       "under `tool-gated-review` was caused by the skill.")
def _(rows):
    rs = baseline_runs(rows, review=True)
    return not any(r["delegated_call"] for r in rs) and rs, dict(n=len(rs))


@claim("delegation-no-quality-gain", "branching", "observed",
       "Delegating did not improve the review on this task: Opus, Sonnet and Codex named both planted bugs in "
       "{b} of {bn} baseline reviews without delegating, and in {s} of {sn} skill runs.")
def _(rows):
    subs = ("claude-opus", "claude-sonnet", CODEX)
    b = [r for r in baseline_runs(rows, review=True) if r["subject"] in subs]
    s = [r for r in skill_runs(rows, skill="tool-gated-review") if r["subject"] in subs]
    bk, sk = sum(r["findings_ok"] for r in b), sum(r["findings_ok"] for r in s)
    return bk / len(b) >= sk / len(s) - 0.05 if b and s else False, dict(b=bk, bn=len(b), s=sk, sn=len(s))


# ---------- Question 2: portability ----------

@claim("portable-identity", "portability", "observed",
       "Vendor and harness branches behaved correctly for both pairs: {ck} of {cn} runs for the Claude models "
       "in Claude Code and {ok} of {on} for Codex with gpt-5.6-luna.")
def _(rows):
    rs = skill_runs(rows, skill="vendor-stamp")
    c = [r for r in rs if r["subject"] in CLAUDE]; o = [r for r in rs if r["subject"] == CODEX]
    f = lambda x: sum(1 for r in x if r["fields"].get("vendor") and r["fields"].get("harness") and r["branch_consistent"])
    return f(c) == len(c) and f(o) == len(o) and rs, dict(ck=f(c), cn=len(c), ok=f(o), on=len(o))


@claim("not-portable-version", "portability", "observed",
       "Branching on an exact model version worked only for the Claude pair ({ck} of {cn} correct) and never "
       "for the Codex pair (0 of {on}).")
def _(rows):
    rs = skill_runs(rows, skill="vendor-stamp")
    c = [r for r in rs if r["subject"] in CLAUDE]; o = [r for r in rs if r["subject"] == CODEX]
    ck, ok = sum(r["fields"].get("model", False) for r in c), sum(r["fields"].get("model", False) for r in o)
    return ck == len(c) and ok == 0, dict(ck=ck, cn=len(c), on=len(o))


@claim("not-portable-tier", "portability", "observed",
       "Branching on tier worked for the Claude pair ({ck} of {cn} loaded tier answers correct) and failed "
       "for the Codex pair (0 of {on}); the difference tracks whether the harness hands the model its exact "
       "model ID, which is inferred, not observed.")
def _(rows):
    rs = [r for r in loaded(skill_runs(rows)) if r["skill"] in TIER_SKILLS]
    c = [r for r in rs if r["subject"] in CLAUDE]; o = [r for r in rs if r["subject"] == CODEX]
    ck = sum(tier_of(r) == gt()[r["subject"]]["tier"] for r in c); ok = sum(tier_of(r) == gt()[CODEX]["tier"] for r in o)
    return ck == len(c) and ok == 0, dict(ck=ck, cn=len(c), on=len(o))


@claim("not-portable-capability-from-knowledge", "portability", "observed",
       "A capability branch answered from product knowledge worked for the Claude pair ({ck} of {cn}) and "
       "only sometimes for the Codex pair ({ok} of {on}), whose answer to the same question varied from run to run.")
def _(rows):
    rs = skill_runs(rows, skill="harness-stamp")
    c = [r for r in rs if r["subject"] in CLAUDE]; o = [r for r in rs if r["subject"] == CODEX]
    ck, ok = sum(r["all_fields_correct"] for r in c), sum(r["all_fields_correct"] for r in o)
    return ck == len(c) and ok < len(o) and rs, dict(ck=ck, cn=len(c), ok=ok, on=len(o))


@claim("partially-portable-capability-from-tools", "portability", "inferred",
       "A capability branch that checks the session's tools produced a delegation for the Claude pair in "
       "{ck} of {cn} runs and for the Codex pair in {ok} of {on}.")
def _(rows):
    rs = skill_runs(rows, skill="tool-gated-review")
    c = [r for r in rs if r["subject"] in CLAUDE]; o = [r for r in rs if r["subject"] == CODEX]
    ck, ok = sum(r["delegated_call"] for r in c), sum(r["delegated_call"] for r in o)
    return ck == len(c) and 0 < ok < len(o), dict(ck=ck, cn=len(c), ok=ok, on=len(o))


@claim("delivery-no-whole-cell-difference-once-loaded", "portability", "observed",
       "Among runs where the skill loaded, no subject-and-skill cell had a whole-cell outcome difference "
       "between deliveries (largest difference {maxdiff} runs in a cell of {cell}); delivery did not change "
       "branch outcomes once the skill was loaded.")
def _(rows):
    rs = loaded(skill_runs(rows))
    cells = defaultdict(lambda: defaultdict(list))
    for r in rs:
        cells[(r["subject"], r["skill"])][r["delivery"]].append(r["outcome_ok"])
    maxdiff, cell, whole = 0, 0, False
    for k, per in cells.items():
        ks = [sum(v) for v in per.values() if len(v) >= 2]
        ns = [len(v) for v in per.values() if len(v) >= 2]
        if len(ks) < 2: continue
        d = max(ks) - min(ks)
        if d > maxdiff: maxdiff, cell = d, max(ns)
        if any(k == n for k, n in zip(ks, ns)) and any(k == 0 for k in ks): whole = True
    return not whole and rs, dict(maxdiff=maxdiff, cell=cell)


@claim("pointer-delivery-portable", "portability", "observed",
       "Pointer delivery (a `CLAUDE.md` / `AGENTS.md` entry) loaded the skill in {k} of {n} pointer runs across "
       "both pairs, against {nk} of {nn} native runs.")
def _(rows):
    p = skill_runs(rows, delivery="pointer"); n = skill_runs(rows, delivery="native")
    return sum(r["triggered"] for r in p) >= sum(r["triggered"] for r in n), \
        dict(k=sum(r["triggered"] for r in p), n=len(p), nk=sum(r["triggered"] for r in n), nn=len(n))


# ---------- Question 3: efficiency ----------

def paired_means(rows, subject, skill_filter, delivery, metric):
    """Mean of `metric` over a subject's loaded skill runs matching skill_filter/delivery, and over their paired baseline runs."""
    rs = [r for r in loaded(skill_runs(rows, subject=subject, delivery=delivery)) if skill_filter(r)]
    base = []
    seen = set()
    for r in rs:
        for b in paired_baseline(rows, r):
            if b["run_id"] not in seen:
                seen.add(b["run_id"]); base.append(b)
    return mean_or_none([r[metric] for r in rs]), mean_or_none([b[metric] for b in base]), len(rs), len(base)


@claim("skill-overhead-tokens", "efficiency", "observed",
       "On the same prompts, every subject processed more input tokens with a native skill than with none: "
       "{table}. (Loaded Study 2 runs against their paired baselines; input tokens include cached input.)")
def _(rows):
    parts, ok, table = [], True, [("subject", "with skill (native)", "no skill", "ratio", "runs")]
    for s in CLAUDE + (CODEX,):
        a, b, na, nb = paired_means(rows, s, lambda r: r["study"] == "work", "native", "tokens_in")
        if a is None or b is None: ok = False; continue
        ratio = a / b
        ok = ok and ratio > 1
        parts.append(f"{s} {a/1000:.0f}k vs {b/1000:.0f}k ({ratio:.1f}x, n={na} vs {nb})")
        table.append((s, f"{a/1000:.0f}k", f"{b/1000:.0f}k", f"{ratio:.1f}x", f"{na} vs {nb}"))
    return ok, dict(table="; ".join(parts), rows=table)


@claim("skill-overhead-tool-invocations", "efficiency", "observed",
       "On the same prompts, every subject made more tool invocations with a native skill than with none: {table}.")
def _(rows):
    parts, ok, table = [], True, [("subject", "with skill (native)", "no skill", "runs")]
    for s in CLAUDE + (CODEX,):
        a, b, na, nb = paired_means(rows, s, lambda r: r["study"] == "work", "native", "tool_invocations")
        if a is None or b is None: ok = False; continue
        ok = ok and a > b
        parts.append(f"{s} {a:.1f} vs {b:.1f} (n={na} vs {nb})")
        table.append((s, f"{a:.1f}", f"{b:.1f}", f"{na} vs {nb}"))
    return ok, dict(table="; ".join(parts), rows=table)


@claim("inline-cheapest-delivery", "efficiency", "observed",
       "In Study 1, where every subject loaded every skill, `inline` used fewer input tokens than both "
       "`native` and `pointer` for every subject: {table}.")
def _(rows):
    parts, ok, table = [], True, [("subject", "inline", "native", "pointer")]
    for s in CLAUDE + (CODEX,):
        m = {d: mean_or_none([r["tokens_in"] for r in loaded(skill_runs(rows, subject=s, delivery=d, study="branch"))]) for d in SKILL_DELIVERIES}
        if any(v is None for v in m.values()): ok = False; continue
        ok = ok and m["inline"] < m["native"] and m["inline"] < m["pointer"]
        parts.append(f"{s} inline {m['inline']/1000:.0f}k, native {m['native']/1000:.0f}k, pointer {m['pointer']/1000:.0f}k")
        table.append((s, f"{m['inline']/1000:.0f}k", f"{m['native']/1000:.0f}k", f"{m['pointer']/1000:.0f}k"))
    return ok, dict(table="; ".join(parts), rows=table)


@claim("pointer-vs-native-cost", "efficiency", "observed",
       "In Study 1, pointer delivery cost more input tokens than native for the Claude models ({claude}) and "
       "less for Codex with gpt-5.6-luna ({codex}); the pointer's extra file read is not the whole story.")
def _(rows):
    def m(s, d): return mean_or_none([r["tokens_in"] for r in loaded(skill_runs(rows, subject=s, delivery=d, study="branch"))])
    cl = [(s, m(s, "pointer"), m(s, "native")) for s in CLAUDE]
    co = (m(CODEX, "pointer"), m(CODEX, "native"))
    ok = all(p and n and p > n for _, p, n in cl) and co[0] and co[1] and co[0] < co[1]
    return ok, dict(claude="; ".join(f"{s} {p/1000:.0f}k vs {n/1000:.0f}k" for s, p, n in cl),
                    codex=f"{co[0]/1000:.0f}k vs {co[1]/1000:.0f}k")


@claim("lighter-branch-cheaper", "efficiency", "observed",
       "Where a subject has a heavy and a light version of its tier branch on the same prompts, the light version "
       "used fewer input tokens: {table}. (Loaded runs, all deliveries; Sonnet's mid branch is identical in both skills.)")
def _(rows):
    # heavy/light per subject: (skill with the heavy branch, skill with the light branch)
    pairs = {"claude-opus": ("tiered-feature", "tiered-guidance"), CODEX: ("tiered-feature", "tiered-guidance"),
             "claude-haiku": ("tiered-guidance", "tiered-feature")}
    parts, ok, table = [], True, [("subject", "light branch", "heavy branch")]
    for s, (heavy, light) in pairs.items():
        h = mean_or_none([r["tokens_in"] for r in loaded(skill_runs(rows, subject=s, skill=heavy))])
        l = mean_or_none([r["tokens_in"] for r in loaded(skill_runs(rows, subject=s, skill=light))])
        if h is None or l is None: ok = False; continue
        ok = ok and l < h
        parts.append(f"{s} light {l/1000:.0f}k vs heavy {h/1000:.0f}k")
        table.append((s, f"{l/1000:.0f}k ({light})", f"{h/1000:.0f}k ({heavy})"))
    return ok, dict(table="; ".join(parts), rows=table)


@claim("delegation-costs-more", "efficiency", "observed",
       "Delegating a review cost more input tokens than reviewing without delegating, within every subject: {table}. "
       "(Delegated skill runs against the same subject's non-delegated runs: its baseline, and for Codex its skill runs that stayed inline.)")
def _(rows):
    parts, ok, table = [], True, [("subject", "delegated", "not delegated")]
    for s in CLAUDE + (CODEX,):
        rev = skill_runs(rows, subject=s, skill="tool-gated-review")
        d = mean_or_none([r["tokens_in"] for r in rev if r["delegated_call"]])
        nd = [r["tokens_in"] for r in rev if not r["delegated_call"]] + [r["tokens_in"] for r in baseline_runs(rows, s, review=True)]
        n = mean_or_none(nd)
        if d is None or n is None: ok = False; continue
        ok = ok and d > n
        parts.append(f"{s} {d/1000:.0f}k vs {n/1000:.0f}k")
        table.append((s, f"{d/1000:.0f}k", f"{n/1000:.0f}k"))
    return ok, dict(table="; ".join(parts), rows=table)


# ---------- Question 4: placement (Study 3) ----------

def gate_runs(rows, skill=None, included=None, delivery=None, subject=None):
    out = [r for r in rows if r["kind"] == "gated"]
    if skill: out = [r for r in out if r["skill"] == skill]
    if included is not None: out = [r for r in out if r["included"] == included]
    if delivery: out = [r for r in out if r["delivery"] in (delivery if isinstance(delivery, tuple) else (delivery,))]
    if subject: out = [r for r in out if r["subject"] in (subject if isinstance(subject, tuple) else (subject,))]
    return out


def select_runs(rows, set_=None, subject=None):
    out = [r for r in rows if r["kind"] == "selection"]
    if set_: out = [r for r in out if r["skill"] == set_]
    if subject: out = [r for r in out if r["subject"] in (subject if isinstance(subject, tuple) else (subject,))]
    return out


def outcome_table(rs, key, values, by=("subject", "delivery")):
    table = [by + values]
    for k in sorted({tuple(r[b] for b in by) for r in rs}):
        cell = [r for r in rs if tuple(r[b] for b in by) == k]
        table.append(k + tuple(str(sum(1 for r in cell if r[key] == v)) for v in values))
    return table


GATE_OUTCOMES = ("not-loaded", "declined", "followed", "ignored", "mixed")


@claim("gate-vendor-keeps-codex-out", "placement", "observed",
       "Under `vendor-gated-guidance` (for Anthropic models only), Codex with gpt-5.6-luna stayed out of the skill "
       "in every native and pointer run ({k} of {n}: not loaded {nl}, declined {d}); it never followed the checklist.")
def _(rows):
    rs = gate_runs(rows, "vendor-gated-guidance", included=False, delivery=LOADABLE, subject=CODEX)
    k = [r for r in rs if r["gate_correct"]]
    c = Counter(r["gate_outcome"] for r in rs)
    return len(k) == len(rs) and rs, dict(k=len(k), n=len(rs), nl=c["not-loaded"], d=c["declined"], rows=outcome_table(rs, "gate_outcome", GATE_OUTCOMES))


@claim("gate-tier-keeps-opus-sonnet-out", "placement", "assumed",
       "Under `tier-gated-guidance` (for small models only), Opus and Sonnet stayed out of the skill in every native "
       "and pointer run ({k} of {n}: not loaded {nl}, declined {d}); the Anthropic tiers are an assumed scale.")
def _(rows):
    rs = gate_runs(rows, "tier-gated-guidance", included=False, delivery=LOADABLE, subject=("claude-opus", "claude-sonnet"))
    k = [r for r in rs if r["gate_correct"]]
    c = Counter(r["gate_outcome"] for r in rs)
    return len(k) == len(rs) and rs, dict(k=len(k), n=len(rs), nl=c["not-loaded"], d=c["declined"], rows=outcome_table(rs, "gate_outcome", GATE_OUTCOMES))


@claim("gate-where-it-held", "placement", "observed",
       "Among the {n} native and pointer runs in which an excluded subject stayed out of a gated skill, the gate held "
       "at the description (skill never loaded) in {nl} and in the body (loaded, then declined) in {d}: {table}.")
def _(rows):
    rs = [r for r in gate_runs(rows, included=False, delivery=LOADABLE) if r["gate_outcome"] in ("not-loaded", "declined")]
    c = Counter(r["gate_outcome"] for r in rs)
    parts = []
    for s in sorted({r["subject"] for r in rs}):
        cc = Counter(r["gate_outcome"] for r in rs if r["subject"] == s)
        parts.append(f"{s} not loaded {cc['not-loaded']}, declined {cc['declined']}")
    return bool(rs), dict(n=len(rs), nl=c["not-loaded"], d=c["declined"], table="; ".join(parts),
                          rows=outcome_table(rs, "gate_outcome", ("not-loaded", "declined"), by=("subject", "skill", "delivery")))


@claim("excluded-never-followed", "placement", "observed",
       "No excluded subject followed a gated skill's checklist in any run, in any delivery ({f} followed or mixed "
       "of {n} runs).")
def _(rows):
    rs = gate_runs(rows, included=False)
    f = [r for r in rs if r["gate_outcome"] in ("followed", "mixed")]
    return len(f) == 0 and rs, dict(f=len(f), n=len(rs))


@claim("bailout-inline", "placement", "observed",
       "With a gated skill's body in the prompt (`inline`), where it cannot be left unloaded, excluded subjects "
       "declined it in {k} of {n} runs: {table}.")
def _(rows):
    rs = gate_runs(rows, included=False, delivery="inline")
    k = [r for r in rs if r["gate_outcome"] == "declined"]
    parts = [f"{s} {sum(1 for r in k if r['subject'] == s)} of {sum(1 for r in rs if r['subject'] == s)}" for s in sorted({r["subject"] for r in rs})]
    return len(k) == len(rs) and rs, dict(k=len(k), n=len(rs), table="; ".join(parts),
                                          rows=outcome_table(rs, "gate_outcome", GATE_OUTCOMES, by=("subject", "skill")))


@claim("included-claude-followed-when-loaded", "placement", "observed",
       "Every Claude model that loaded a gated skill it was included under followed its checklist ({k} of {n} loaded "
       "runs, all deliveries): {table}. The Codex pair's included runs are covered by `gate-tier-codex-refuses-own-skill`.")
def _(rows):
    rs = [r for r in gate_runs(rows, included=True, subject=CLAUDE) if r["triggered"]]
    k = [r for r in rs if r["gate_outcome"] == "followed"]
    parts = [f"{s} {sum(1 for r in k if r['subject'] == s)} of {sum(1 for r in rs if r['subject'] == s)}" for s in sorted({r["subject"] for r in rs})]
    return len(k) == len(rs) and rs, dict(k=len(k), n=len(rs), table="; ".join(parts),
                                          rows=outcome_table(rs, "gate_outcome", GATE_OUTCOMES, by=("subject", "skill", "delivery")))


@claim("included-loading", "placement", "observed",
       "Included subjects loaded the gated skill written for them in {k} of {n} native and pointer runs: {table}.")
def _(rows):
    rs = gate_runs(rows, included=True, delivery=LOADABLE)
    k = [r for r in rs if r["triggered"]]
    parts = [f"{s} {sum(1 for r in k if r['subject'] == s and r['skill'] == sk)} of {sum(1 for r in rs if r['subject'] == s and r['skill'] == sk)} ({sk})"
             for s in sorted({r["subject"] for r in rs}) for sk in GATED_SKILLS if any(r["subject"] == s and r["skill"] == sk for r in rs)]
    return bool(rs), dict(k=len(k), n=len(rs), table="; ".join(parts),
                          rows=outcome_table(rs, "gate_outcome", GATE_OUTCOMES, by=("subject", "skill", "delivery")))


@claim("haiku-loading-limits-gates", "placement", "observed",
       "Haiku's loading failure, not the gate, decided its Study 3 outcomes: included under both gated skills, it loaded "
       "them in {gn} of {gnn} native and {gp} of {gpn} pointer runs and followed them in {gi} of {gin} inline runs; with a "
       "selection set it followed a skill in {sn} of {snn} native and {sp} of {spn} pointer runs, and every choice it made "
       "was correct ({sc} of {sch}).")
def _(rows):
    g = gate_runs(rows, included=True, subject="claude-haiku")
    s = select_runs(rows, subject="claude-haiku")
    def cnt(rs, d, pred): sel = [r for r in rs if r["delivery"] == d]; return sum(pred(r) for r in sel), len(sel)
    gn, gnn = cnt(g, "native", lambda r: r["triggered"]); gp, gpn = cnt(g, "pointer", lambda r: r["triggered"])
    gi, gin = cnt(g, "inline", lambda r: r["gate_outcome"] == "followed")
    sn, snn = cnt(s, "native", lambda r: r["selection_outcome"] != "none"); sp, spn = cnt(s, "pointer", lambda r: r["selection_outcome"] != "none")
    chose = [r for r in s if r["selection_outcome"] != "none"]; sc = sum(r["selection_outcome"] == "correct" for r in chose)
    ok = gn < gnn and gp < gpn and gi == gin and sn < snn and sp == spn and sc == len(chose) and g and s
    return ok, dict(gn=gn, gnn=gnn, gp=gp, gpn=gpn, gi=gi, gin=gin, sn=sn, snn=snn, sp=sp, spn=spn, sc=sc, sch=len(chose))


@claim("gate-tier-codex-refuses-own-skill", "placement", "observed",
       "Codex with gpt-5.6-luna, whose documented tier is small, stayed out of `tier-gated-guidance`, the skill written "
       "for small models, in {k} of {n} native and pointer runs (not loaded {nl}, declined {d}), and declined it in "
       "{ik} of {inn} inline runs; a skill reserved for weaker models cannot rest on its self-placement.")
def _(rows):
    rs = gate_runs(rows, "tier-gated-guidance", delivery=LOADABLE, subject=CODEX)
    k = [r for r in rs if r["gate_outcome"] in ("not-loaded", "declined")]
    c = Counter(r["gate_outcome"] for r in rs)
    inl = gate_runs(rows, "tier-gated-guidance", delivery="inline", subject=CODEX)
    ik = [r for r in inl if r["gate_outcome"] == "declined"]
    ex = excerpts(k + ik, r"flagship|not a small|mid-tier|tier", limit=2)
    return len(k) == len(rs) and rs, dict(k=len(k), n=len(rs), nl=c["not-loaded"], d=c["declined"], ik=len(ik), inn=len(inl)), ex


@claim("select-vendor-correct", "placement", "observed",
       "Given `feature-anthropic` and `feature-openai` side by side, every run that followed a skill followed the one "
       "for its vendor ({k} of {n} runs that chose; {none} chose none): {table}.")
def _(rows):
    rs = select_runs(rows, "select-vendor")
    chose = [r for r in rs if r["selection_outcome"] != "none"]
    k = [r for r in chose if r["selection_outcome"] == "correct"]
    return len(k) == len(chose) and chose, dict(k=len(k), n=len(chose), none=len(rs) - len(chose),
                                                 table=fmt_counts(Counter(r["selection_outcome"] for r in rs)),
                                                 rows=outcome_table(rs, "selection_outcome", ("correct", "wrong", "several", "none")))


@claim("select-tier-claude-correct", "placement", "assumed",
       "Given `feature-flagship`, `feature-mid` and `feature-small` side by side, every Claude model run that followed a "
       "skill followed the one for its tier ({k} of {n} runs that chose; {none} chose none); the tiers are an assumed scale.")
def _(rows):
    rs = select_runs(rows, "select-tier", subject=CLAUDE)
    chose = [r for r in rs if r["selection_outcome"] != "none"]
    k = [r for r in chose if r["selection_outcome"] == "correct"]
    return len(k) == len(chose) and chose, dict(k=len(k), n=len(chose), none=len(rs) - len(chose),
                                                 rows=outcome_table(rs, "selection_outcome", ("correct", "wrong", "several", "none")))


@claim("select-tier-codex-wrong", "placement", "observed",
       "Codex with gpt-5.6-luna never followed `feature-small`, the skill for its documented tier (0 of {n} runs that "
       "chose); it followed {answers}.")
def _(rows):
    rs = select_runs(rows, "select-tier", subject=CODEX)
    chose = [r for r in rs if r["selection_outcome"] != "none"]
    small = [r for r in chose if r["chosen_skill"] == "feature-small"]
    answers = Counter(", ".join(r["skills_followed"]) for r in chose)
    return len(small) == 0 and chose, dict(n=len(chose), answers=fmt_counts(answers))


@claim("select-loading", "placement", "observed",
       "With a selection set installed, subjects followed at least one of its skills in {k} of {n} runs: {table}.")
def _(rows):
    rs = select_runs(rows)
    k = [r for r in rs if r["selection_outcome"] != "none"]
    parts = [f"{s} {sum(1 for r in k if r['subject'] == s and r['delivery'] == d)} of {sum(1 for r in rs if r['subject'] == s and r['delivery'] == d)} ({d})"
             for s in sorted({r["subject"] for r in rs}) for d in LOADABLE if any(r["subject"] == s and r["delivery"] == d for r in rs)]
    return bool(rs), dict(k=len(k), n=len(rs), table="; ".join(parts))


@claim("select-reads-before-choosing", "placement", "observed",
       "In {k} of {n} selection runs that followed exactly one skill, the agent had read at least one other alternative "
       "first (the Claude pair {ck} of {cn}, the Codex pair {ok} of {on}).")
def _(rows):
    rs = [r for r in select_runs(rows) if r["selection_outcome"] in ("correct", "wrong")]
    k = [r for r in rs if r["read_only"]]
    c = [r for r in rs if r["subject"] in CLAUDE]; o = [r for r in rs if r["subject"] == CODEX]
    return bool(rs), dict(k=len(k), n=len(rs), ck=sum(bool(r["read_only"]) for r in c), cn=len(c),
                          ok=sum(bool(r["read_only"]) for r in o), on=len(o))


@claim("select-work-matches-choice", "placement", "observed",
       "In every selection run that followed exactly one skill, the work matched that skill's body ({k} of {n}).")
def _(rows):
    rs = [r for r in select_runs(rows) if r["selection_outcome"] in ("correct", "wrong")]
    k = [r for r in rs if r["work_matches_choice"]]
    return len(k) == len(rs) and rs, dict(k=len(k), n=len(rs))


@claim("portable-gate-vendor", "portability", "observed",
       "A gate on vendor behaved correctly for both pairs in native and pointer runs: the Claude pair, included, followed "
       "the skill whenever it loaded ({ck} of {cn} loaded runs) and the Codex pair, excluded, stayed out ({ok} of {on}).")
def _(rows):
    c = [r for r in gate_runs(rows, "vendor-gated-guidance", delivery=LOADABLE, subject=CLAUDE) if r["triggered"]]
    o = gate_runs(rows, "vendor-gated-guidance", delivery=LOADABLE, subject=CODEX)
    ck, ok = sum(r["gate_outcome"] == "followed" for r in c), sum(r["gate_correct"] for r in o)
    return ck == len(c) and ok == len(o) and c and o, dict(ck=ck, cn=len(c), ok=ok, on=len(o))


@claim("not-portable-gate-tier", "portability", "observed",
       "A gate on tier behaved correctly for the Claude pair ({ck} of {cn} native and pointer runs) and not for the Codex "
       "pair ({ok} of {on}), which refused the skill written for its documented tier.")
def _(rows):
    c = gate_runs(rows, "tier-gated-guidance", delivery=LOADABLE, subject=CLAUDE)
    o = gate_runs(rows, "tier-gated-guidance", delivery=LOADABLE, subject=CODEX)
    # Haiku's loading failures are a delivery matter, not a gate failure: credit an included run that loaded and followed, or did not load
    ck = sum(r["gate_correct"] or (r["included"] and not r["triggered"]) for r in c)
    ok = sum(r["gate_correct"] for r in o)
    return ck == len(c) and ok < len(o) and c and o, dict(ck=ck, cn=len(c), ok=ok, on=len(o))


@claim("portable-selection-vendor", "portability", "observed",
       "Selection by vendor worked for both pairs among runs that chose: the Claude pair {ck} of {cn}, the Codex pair {ok} of {on}.")
def _(rows):
    c = [r for r in select_runs(rows, "select-vendor", CLAUDE) if r["selection_outcome"] != "none"]
    o = [r for r in select_runs(rows, "select-vendor", CODEX) if r["selection_outcome"] != "none"]
    ck, ok = sum(r["selection_outcome"] == "correct" for r in c), sum(r["selection_outcome"] == "correct" for r in o)
    return ck == len(c) and ok == len(o) and c and o, dict(ck=ck, cn=len(c), ok=ok, on=len(o))


@claim("not-portable-selection-tier", "portability", "observed",
       "Selection by tier worked for the Claude pair ({ck} of {cn} runs that chose) and not for the Codex pair ({ok} of {on}).")
def _(rows):
    c = [r for r in select_runs(rows, "select-tier", CLAUDE) if r["selection_outcome"] != "none"]
    o = [r for r in select_runs(rows, "select-tier", CODEX) if r["selection_outcome"] != "none"]
    ck, ok = sum(r["selection_outcome"] == "correct" for r in c), sum(r["selection_outcome"] == "correct" for r in o)
    return ck == len(c) and ok < len(o) and c and o, dict(ck=ck, cn=len(c), ok=ok, on=len(o))


@claim("staying-out-costs-baseline", "efficiency", "observed",
       "A run in which the gate held at the description cost about what the no-skill baseline of the same prompt cost, "
       "and one that loaded the skill and then declined cost more: {table}. (Input tokens, per subject; excluded subjects only.)")
def _(rows):
    parts, ok, table = [], True, [("subject", "not loaded", "declined", "no skill")]
    for s in CLAUDE + (CODEX,):
        rs = gate_runs(rows, included=False, subject=s)
        nl = mean_or_none([r["tokens_in"] for r in rs if r["gate_outcome"] == "not-loaded"])
        d = mean_or_none([r["tokens_in"] for r in rs if r["gate_outcome"] == "declined"])
        b = mean_or_none([x["tokens_in"] for r in rs for x in paired_baseline(rows, r)])
        if b is None or (nl is None and d is None): continue
        if nl is not None: ok = ok and nl <= 1.25 * b
        if nl is not None and d is not None: ok = ok and d > nl
        f = lambda v: f"{v/1000:.0f}k" if v is not None else "-"
        parts.append(f"{s} not loaded {f(nl)}, declined {f(d)}, no skill {f(b)}")
        table.append((s, f(nl), f(d), f(b)))
    return ok and parts, dict(table="; ".join(parts), rows=table)


# ---------- evaluation ----------

def evaluate(rows):
    out = []
    for c in CLAIMS:
        try:
            res = c["check"](rows)
            holds, values = res[0], res[1]
            exhibits = res[2] if len(res) > 2 else []
            holds = bool(holds)
            statement = c["statement"].format(**values)
        except Exception as e:  # a claim that cannot be computed fails loudly, never silently
            holds, values, exhibits, statement = False, {"error": str(e)}, [], f"{c['statement']} (could not be computed: {e})"
        out.append(dict(id=c["id"], question=c["question"], kind=c["kind"], holds=holds, values=values,
                        statement=statement, exhibits=exhibits))
    return out


def fingerprint(rows):
    keyed = sorted((r["run_id"], json.dumps({k: r.get(k) for k in OUTCOME_FIELDS}, sort_keys=True)) for r in rows)
    return hashlib.sha256(json.dumps(keyed).encode()).hexdigest()[:16]
