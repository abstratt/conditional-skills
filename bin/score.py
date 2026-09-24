#!/usr/bin/env python3
"""Deterministic scoring of every run: trigger evidence, outcome checks, stamp values, cost."""
import ast, json, re, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from common import *


def events(run_dir):
    for line in (run_dir / "stdout.jsonl").read_text().splitlines():
        try:
            yield json.loads(line)
        except json.JSONDecodeError:
            pass


def claude_evidence(run_dir, skills):
    """Loading evidence per skill (a run may install a set); `skill_invoked`/`skill_read` summarise over the set."""
    ev = dict(skill_invoked=False, skill_read=False, skills_invoked=[], skills_read=[], tool_calls=[], tool_invocations=0,
              final="", cost_usd=None, tokens_in=0, tokens_out=0, turns=None, duration_ms=None)
    for e in events(run_dir):
        if e.get("type") == "assistant":
            for b in e.get("message", {}).get("content", []):
                if b.get("type") == "tool_use":
                    ev["tool_invocations"] += 1
                    inp = json.dumps(b.get("input", {}))
                    ev["tool_calls"].append(f'{b["name"]} {inp[:200]}')
                    if b["name"] == "Skill" and b["input"].get("skill") in skills:
                        ev["skill_invoked"] = True
                        ev["skills_invoked"].append(b["input"]["skill"])
                    if "SKILL.md" in inp:
                        ev["skill_read"] = True
                        ev["skills_read"] += [s for s in skills if f"{s}/SKILL.md" in inp]
        elif e.get("type") == "result":
            ev["final"] = e.get("result") or ""
            ev["cost_usd"] = e.get("total_cost_usd")
            ev["turns"] = e.get("num_turns")
            ev["duration_ms"] = e.get("duration_ms")
            u = e.get("usage", {})
            ev["tokens_in"] = (u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0)
                               + u.get("cache_read_input_tokens", 0))
            ev["tokens_out"] = u.get("output_tokens", 0)
    return ev


def codex_evidence(run_dir, skills):
    # Codex reports no turn count; tool invocations are the step count both harnesses expose
    ev = dict(skill_invoked=False, skill_read=False, skills_invoked=[], skills_read=[], skill_mentioned=False, tool_calls=[],
              tool_invocations=0, final="", cost_usd=None, tokens_in=0, tokens_out=0, turns=None, duration_ms=None)
    for e in events(run_dir):
        if e.get("type") == "item.completed":
            it = e["item"]
            if it["type"] not in ("agent_message", "reasoning", "error"):  # commands, file edits, subagent calls, web searches, ...
                ev["tool_invocations"] += 1
            if it["type"] == "command_execution":
                ev["tool_calls"].append("cmd " + (it.get("command") or "")[:200])
                cmd = it.get("command") or ""
                if "SKILL.md" in cmd:
                    ev["skill_read"] = True
                    ev["skills_read"] += [s for s in skills if f"{s}/SKILL.md" in cmd]
            elif it["type"] == "file_change":
                ev["tool_calls"].append("file_change " + json.dumps(it.get("changes", ""))[:200])
            elif it["type"] == "agent_message":
                ev["final"] = it.get("text", "")
                if any(s in ev["final"] for s in skills):
                    ev["skill_mentioned"] = True
            elif it["type"] not in ("reasoning", "error"):
                ev["tool_calls"].append(it["type"] + " " + json.dumps(it)[:160])
        elif e.get("type") == "turn.completed":
            u = e.get("usage", {})
            ev["tokens_in"] += u.get("input_tokens", 0)
            ev["tokens_out"] += u.get("output_tokens", 0)
    lm = run_dir / "last_message.txt"
    if lm.exists() and lm.read_text().strip():
        ev["final"] = lm.read_text()
    return ev


def validity(run_dir, meta):
    """Split infrastructure failures from agent behaviour. An invalid run's outcome is unusable and it
    is excluded and rerun; a run whose timing is invalid keeps its outcome but is left out of time comparisons."""
    evs = list(events(run_dir)) if (run_dir / "stdout.jsonl").exists() else []
    reason = None
    if meta.get("timed_out"):
        reason = "timed out"
    elif meta["harness"] == "claude-code":
        res = [e for e in evs if e.get("type") == "result"]
        if not res:
            reason = "no final result"
        elif res[-1].get("is_error") and res[-1].get("subtype") != "error_max_turns":
            reason = "error result: " + str(res[-1].get("result"))[:80]
    else:
        types = [e.get("type") for e in evs]
        if "turn.failed" in types:
            reason = "turn failed"
        elif "turn.completed" not in types:
            reason = "no completed turn"
        elif meta.get("exit_code") != 0:
            reason = f"exit code {meta.get('exit_code')}"
    timing = None
    if "active_s" in meta and meta["wall_s"] - meta["active_s"] > 30:
        timing = "machine slept during the run"
    elif "active_s" not in meta and meta["wall_s"] > meta.get("timeout", 600) + 30:
        # older runs lack active_s; the run timeout uses a clock that stops during sleep,
        # so wall time beyond it means the machine slept
        timing = "machine slept during the run"
    elif any(e.get("type") == "error" and "Reconnecting" in str(e.get("message")) for e in evs):
        timing = "network reconnects during the run"
    return dict(valid=reason is None, invalid_reason=reason, timing_valid=timing is None, timing_invalid_reason=timing)


def parse_kv(path):
    out = {}
    if path.exists():
        for line in path.read_text().splitlines():
            if ":" in line:
                k, _, v = line.partition(":")
                out[k.strip().lower()] = v.split("#")[0].strip().lower()
    return out


def check_outcome(ws, spec, final):
    checks = {}
    if "file_regex" in spec:
        f, rx = spec["file_regex"]
        p = ws / f
        checks["file_regex"] = p.exists() and re.search(rx, p.read_text()) is not None
    if "file_absent" in spec:
        checks["file_absent"] = not (ws / spec["file_absent"]).exists()
    if "final_regex" in spec:
        checks["final_regex"] = re.search(spec["final_regex"], final) is not None
    return checks


def changed_files(ws):
    out = subprocess.run(["git", "status", "--porcelain"], cwd=ws, capture_output=True, text=True).stdout
    return sorted(l[3:].strip() for l in out.splitlines() if l.strip() and "__pycache__" not in l)


TEST_RUNNER = r"""
import sys, types, contextlib, importlib.util, inspect
sys.path.insert(0, '.')
fake = types.ModuleType('pytest')
@contextlib.contextmanager
def raises(exc, *a, **k):
    try:
        yield
    except exc:
        return
    raise AssertionError('did not raise')
fake.raises = raises
fake.approx = lambda x, *a, **k: x
sys.modules['pytest'] = fake
spec = importlib.util.spec_from_file_location('test_app', 'tests/test_app.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
bad = []
for n, f in inspect.getmembers(m, inspect.isfunction):
    if n.startswith('test_') and not inspect.signature(f).parameters:
        try:
            f()
        except Exception as e:
            bad.append(f'{n}: {e!r}')
print('\n'.join(bad)); sys.exit(1 if bad else 0)
"""


def run_check(ws, code):
    r = subprocess.run([sys.executable, "-c", code], cwd=ws, capture_output=True, text=True, timeout=60)
    return r.returncode == 0, (r.stderr or r.stdout)[-300:]


def has_docstring(app, func):
    try:
        tree = ast.parse(app)
    except SyntaxError:
        return False
    return any(isinstance(n, ast.FunctionDef) and n.name == func and ast.get_docstring(n) for n in ast.walk(tree))


def tier_from_work(skill, n, doc, todo):
    if skill == "tiered-feature":
        return "flagship" if n >= 3 else "mid" if 1 <= n <= 2 else "small" if todo else None
    return "small" if n >= 3 else "mid" if 1 <= n <= 2 else "flagship" if not doc else None


def feature_work(ws, prompt):
    """What the agent did to the feature: test count, docstring, TODO marker, feature check, test run."""
    app = (ws / "src" / "app.py").read_text() if (ws / "src" / "app.py").exists() else ""
    tests = ws / "tests" / "test_app.py"
    n = len(re.findall(r"^\s*def test_", tests.read_text(), re.M)) if tests.exists() else 0
    todo = "TODO(review)" in app
    doc = has_docstring(app, re.search(r"import (\w+)", prompt["python_check"]).group(1))
    ok, err = run_check(ws, prompt["python_check"])
    tests_pass = run_check(ws, TEST_RUNNER)[0] if tests.exists() else None
    return dict(n_tests=n, docstring=doc, todo=todo, feature_ok=ok, feature_err=err, tests_pass=tests_pass)


def trace_lines(ws):
    p = ws / ".skill-trace"
    return [l.strip() for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def score_gate(s, ws, prompt, sub_gt, ev):
    """Study 3 (DESIGN.md): the gate outcome for a gated skill, or the selection outcome for a set."""
    lines = trace_lines(ws)
    s.update(feature_work(ws, prompt))
    if prompt["kind"] == "gated":
        skill = prompt["skill"]
        (field, value), = prompt["gate"].items()
        included = sub_gt[field] == value
        checklist = bool(s["docstring"] and s["n_tests"] >= 3 and s["tests_pass"])
        declined_line, plain_line = f"{skill}: declined" in lines, skill in lines
        if not s["triggered"]:
            outcome = "not-loaded"
        elif declined_line and not plain_line and not checklist:
            outcome = "declined"
        elif plain_line and not declined_line and checklist:
            outcome = "followed"
        elif not declined_line and not plain_line and not checklist:
            outcome = "ignored"
        else:
            outcome = "mixed"
        correct = outcome == "followed" if included else outcome in ("not-loaded", "declined")
        s.update(gate_field=field, gate_value=value, included=included, checklist_done=checklist,
                 declined_line=declined_line, gate_outcome=outcome, gate_correct=correct)
        s["trigger_correct"] = correct
        s["outcome_ok"] = correct and s["feature_ok"]
    else:
        skills = prompt["skills"]
        by = prompt["select_by"]
        expected = f"feature-{sub_gt[by]}"
        markers = {k for k in skills if (ws / f"picked-{k}.txt").exists()}
        followed = sorted(k for k in skills if k in lines or k in markers)
        loaded = sorted(set(followed) | set(ev["skills_invoked"]) | set(ev["skills_read"]))
        outcome = ("correct" if followed == [expected] else "none" if not followed
                   else "several" if len(followed) > 1 else "wrong")
        chosen = followed[0] if len(followed) == 1 else None
        body = {"feature-anthropic": "mid", "feature-openai": "mid", "feature-flagship": "flagship",
                "feature-mid": "mid", "feature-small": "small"}
        implied = tier_from_work("tiered-feature", s["n_tests"], s["docstring"], s["todo"])
        s.update(select_by=by, expected_skill=expected, skills_loaded=loaded, skills_followed=followed,
                 read_only=sorted(set(loaded) - set(followed)), chosen_skill=chosen, selection_outcome=outcome,
                 implied_tier=implied, work_matches_choice=chosen is not None and implied == body[chosen])
        s["triggered"] = bool(loaded)
        s["trigger_correct"] = s["triggered"]
        s["outcome_ok"] = outcome == "correct" and s["work_matches_choice"] and s["feature_ok"]


def delegated(tool_calls):
    return any(tc.split(" ")[0] in ("Task", "Agent") or "spawn" in tc.lower() or "collab" in tc.lower()
               for tc in tool_calls)


def score_work(s, ws, prompt, skill, sub_gt):
    if prompt["kind"] == "baseline" and "outcome" in prompt:
        # no skill: does the model delegate a review unprompted, and does it find both planted bugs?
        written = "".join((ws / f).read_text(errors="ignore") for f in s["changed_files"]
                          if not f.startswith("src/") and (ws / f).is_file())
        s.update(delegated_call=delegated(s["tool_calls"]),
                 findings_ok=re.search(prompt["outcome"]["file_regex"][1], s["final"] + "\n" + written) is not None,
                 src_untouched=not any(f.startswith("src/") for f in s["changed_files"]))
        s["outcome_ok"] = s["findings_ok"]
    elif prompt["kind"] == "baseline":
        # no skill: record what the model does unprompted, and which tier each skill would read it as
        app = (ws / "src" / "app.py").read_text() if (ws / "src" / "app.py").exists() else ""
        tests = ws / "tests" / "test_app.py"
        n = len(re.findall(r"^\s*def test_", tests.read_text(), re.M)) if tests.exists() else 0
        todo = "TODO(review)" in app
        doc = has_docstring(app, re.search(r"import (\w+)", prompt["python_check"]).group(1))
        ok, err = run_check(ws, prompt["python_check"])
        tests_pass = run_check(ws, TEST_RUNNER)[0] if tests.exists() else None
        s.update(n_tests=n, docstring=doc, todo=todo, feature_ok=ok, feature_err=err, tests_pass=tests_pass,
                 reads_as_feature=tier_from_work("tiered-feature", n, doc, todo),
                 reads_as_guidance=tier_from_work("tiered-guidance", n, doc, todo))
        s["outcome_ok"] = ok
    elif skill in ("tiered-feature", "tiered-guidance"):
        reported = parse_kv(ws / "TIER.txt").get("tier")
        app = (ws / "src" / "app.py").read_text() if (ws / "src" / "app.py").exists() else ""
        tests = ws / "tests" / "test_app.py"
        n = len(re.findall(r"^\s*def test_", tests.read_text(), re.M)) if tests.exists() else 0
        todo = "TODO(review)" in app
        doc = has_docstring(app, re.search(r"import (\w+)", prompt["python_check"]).group(1))
        implied = tier_from_work(skill, n, doc, todo)
        ok, err = run_check(ws, prompt["python_check"])
        tests_pass = None
        if tests.exists():
            tests_pass, _ = run_check(ws, TEST_RUNNER)
        truth = sub_gt["tier"]
        s.update(reported_tier=reported, implied_tier=implied, n_tests=n, todo=todo, docstring=doc,
                 feature_ok=ok, feature_err=err, tests_pass=tests_pass, report_matches_truth=reported == truth,
                 work_matches_report=implied is not None and implied == reported, work_matches_truth=implied == truth)
        s["outcome_ok"] = ok and s["work_matches_report"] and s["report_matches_truth"]
    else:
        rv = ws / "REVIEW.md"
        first = rv.read_text().strip().splitlines()[0] if rv.exists() and rv.read_text().strip() else ""
        mode = first.partition(":")[2].strip().lower() if first.lower().startswith("mode:") else None
        delegated_call = delegated(s["tool_calls"])
        truth = sub_gt["subagents_session"] == "yes"
        findings = check_outcome(ws, prompt.get("outcome", {}), s["final"])
        s.update(mode=mode, delegated_call=delegated_call, mode_matches_truth=(mode == "delegated") == truth,
                 mode_consistent=(mode == "delegated") == delegated_call,
                 findings_ok=all(findings.values()) if findings else False,
                 src_untouched=not any(f.startswith("src/") for f in s["changed_files"]))
        s["outcome_ok"] = s["mode_matches_truth"] and s["mode_consistent"] and s["findings_ok"] and s["src_untouched"]


def score(run_dir):
    meta = read_json(run_dir / "meta.json")
    if not meta:
        return None
    ws = run_dir / "workspace"
    prompt, skill = meta["prompt"], meta["prompt"]["skill"]
    skills = prompt_skills(prompt)
    gt = ground_truth()
    sub_gt = gt["subjects"][meta["subject"]]
    ev = (claude_evidence if meta["harness"] == "claude-code" else codex_evidence)(run_dir, skills)
    trace = (ws / ".skill-trace").read_text() if (ws / ".skill-trace").exists() else ""
    s = dict(run_id=meta["run_id"], subject=meta["subject"], harness=meta["harness"], delivery=meta["delivery"],
             study=prompt["study"], prompt_id=prompt["id"], kind=prompt["kind"], skill=skill, rep=meta["rep"],
             expect_trigger=prompt["expect_trigger"], exit_code=meta.get("exit_code"), timed_out=meta.get("timed_out"),
             trace_hit=any(k in trace for k in skills), skill_invoked=ev["skill_invoked"], skill_read=ev["skill_read"],
             skill_mentioned=ev.get("skill_mentioned"), changed_files=changed_files(ws),
             cost_usd=ev["cost_usd"], tokens_in=ev["tokens_in"], tokens_out=ev["tokens_out"], turns=ev["turns"], tool_invocations=ev["tool_invocations"],
             wall_s=meta.get("wall_s"), final=ev["final"], tool_calls=ev["tool_calls"], **validity(run_dir, meta))
    s["triggered"] = bool(s["trace_hit"] or s["skill_invoked"] or s["skill_read"])
    if meta["delivery"] == "inline":  # the instructions are in the prompt, so loading cannot fail
        s["triggered"] = True
    s["trigger_correct"] = s["triggered"] == prompt["expect_trigger"]
    if prompt["study"] == "work":
        score_work(s, ws, prompt, skill, sub_gt)
    elif prompt["study"] == "gate":
        score_gate(s, ws, prompt, sub_gt, ev)
    else:
        stamp = {"vendor-stamp": "AGENT.txt", "harness-stamp": "HARNESS.txt", "tier-stamp": "TIER.txt"}[skill]
        kv = parse_kv(ws / stamp)
        s["stamp"] = kv
        fields = {}
        if skill == "vendor-stamp":
            fields["vendor"] = kv.get("vendor") == sub_gt["vendor"]
            fields["harness"] = kv.get("harness") == sub_gt["harness"]
            fields["model"] = any(t in kv.get("model", "") for t in sub_gt["model_tokens"])
            key, reported = "vendor", kv.get("vendor")
        elif skill == "harness-stamp":
            fields["subagents"] = kv.get("subagents") == sub_gt["subagents"]
            key, reported = "subagents", kv.get("subagents")
        else:
            fields["tier"] = kv.get("tier") == sub_gt["tier"]
            key, reported = "tier", kv.get("tier")
        bf = gt["branch_files"][key]
        truth_file = bf[sub_gt[key]]
        reported_file = bf.get(reported, bf.get("other")) if reported else None
        s["fields"] = fields
        s["stamp_present"] = bool(kv)
        s["fields_correct"] = sum(fields.values())
        s["fields_total"] = len(fields)
        s["all_fields_correct"] = all(fields.values()) and bool(fields)
        s["branch_matches_truth"] = (ws / truth_file).exists()
        s["branch_consistent"] = bool(reported_file) and (ws / reported_file).exists() and \
            all(not (ws / f).exists() for f in bf.values() if f != reported_file)
        if skill == "tier-stamp" and reported_file and (ws / reported_file).exists():
            n = len([l for l in (ws / reported_file).read_text().splitlines() if l.strip()])
            s["branch_content_ok"] = n == {"deep.txt": 3, "mid.txt": 2, "lite.txt": 1}[reported_file]
        s["outcome_ok"] = s["all_fields_correct"] and s["branch_consistent"]
    (run_dir / "score.json").write_text(json.dumps(s, indent=2))
    return s


if __name__ == "__main__":
    n = 0
    for d in run_dirs():
        s = score(d)
        if s:
            n += 1
            print(f'{s["run_id"]}: triggered={s["triggered"]} correct={s["trigger_correct"]} '
                  f'outcome_ok={s.get("outcome_ok")} cost={s["cost_usd"]} tokens={s["tokens_in"]}/{s["tokens_out"]} '
                  f'wall={s["wall_s"]}s')
    print(f"scored {n} runs", file=sys.stderr)
