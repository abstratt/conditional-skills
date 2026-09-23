#!/usr/bin/env python3
"""Drive one run per (subject, delivery, prompt, rep) cell, headless, in a fresh workspace."""
import argparse, json, os, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from common import *

CODEX_HOME_SRC = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
# Codex looks for helper binaries next to argv[0]; resolve symlinks so they are found.
CODEX_BIN = os.path.realpath(shutil.which("codex"))


def seed_workspace(ws, seed="seed"):
    shutil.copytree(ROOT / seed, ws)
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=ws, check=True)
    subprocess.run(["git", "-c", "user.name=exp", "-c", "user.email=exp@example.com",
                    "commit", "-q", "--allow-empty", "-m", "seed"], cwd=ws, check=True)
    subprocess.run(["git", "add", "-A"], cwd=ws, check=True)
    subprocess.run(["git", "-c", "user.name=exp", "-c", "user.email=exp@example.com",
                    "commit", "-q", "-m", "seed files"], cwd=ws, check=True)


def pointer_block(skills):
    lines = [f"- `{s}`: {skill_frontmatter(s)[0]['description']} File: `skills/{s}/SKILL.md`" for s in skills]
    return (f"# Project instructions\n\n## Skills\n\nThis project ships skills as files. "
            f"Before acting on a request that a skill covers, read its SKILL.md and follow it.\n\n"
            + "\n".join(lines) + "\n")


def inline_prompt(skill, request):
    # the skill body, without frontmatter, given as instructions ahead of the request
    _, text = skill_frontmatter(skill)
    body = text.split("---\n", 2)[2].strip()
    return (f"Follow these instructions for the request below.\n\n<instructions>\n{body}\n</instructions>\n\n"
            f"Request: {request}")


def install_skills(ws, codex_home, harness, delivery, skills):
    """Install one skill, or a selection set of several, natively or behind a pointer file."""
    for skill in skills:
        src = ROOT / "skills" / skill
        if delivery == "native":
            if harness == "claude-code":
                shutil.copytree(src, ws / ".claude" / "skills" / skill)
            else:
                shutil.copytree(src, codex_home / "skills" / skill)
        else:
            shutil.copytree(src, ws / "skills" / skill)
    if delivery == "pointer":
        name = "CLAUDE.md" if harness == "claude-code" else "AGENTS.md"
        (ws / name).write_text(pointer_block(skills))
    # commit the installed files so scoring can diff against them
    subprocess.run(["git", "add", "-A"], cwd=ws, check=True)
    subprocess.run(["git", "-c", "user.name=exp", "-c", "user.email=exp@example.com",
                    "commit", "-q", "--allow-empty", "-m", "install skill"], cwd=ws, check=True)


def make_codex_home(codex_home, model, ws):
    codex_home.mkdir(parents=True)
    (codex_home / "skills").mkdir()
    os.symlink(CODEX_HOME_SRC / "auth.json", codex_home / "auth.json")
    (codex_home / "config.toml").write_text(
        f'model = "{model}"\nmodel_reasoning_effort = "high"\napproval_policy = "never"\n'
        f'sandbox_mode = "workspace-write"\n\n[projects."{ws}"]\ntrust_level = "trusted"\n')


def claude_cmd(model, prompt, max_turns):
    return ["claude", "-p", prompt, "--model", model, "--output-format", "stream-json", "--verbose",
            "--dangerously-skip-permissions", "--setting-sources", "project", "--strict-mcp-config",
            "--no-session-persistence", "--max-turns", str(max_turns)]


def codex_cmd(model, ws, run_dir):
    return [CODEX_BIN, "exec", "--json", "--skip-git-repo-check", "--ephemeral", "--color", "never",
            "-C", str(ws), "-s", "workspace-write", "-m", model,
            "-o", str(run_dir / "last_message.txt"), "-"]


def do_run(cell, args):
    subject, delivery, prompt, rep = cell
    sub = SUBJECTS[subject]
    run_id = f"{subject}__{delivery}__{prompt['id']}__r{rep}"
    run_dir = RUNS / run_id
    if run_dir.exists() and not args.force:
        # a run dir without meta.json was interrupted before it finished: always redo it
        score = read_json(run_dir / "score.json", {}) or {}
        if (run_dir / "meta.json").exists() and not (args.rerun_invalid and score.get("valid") is False):
            return run_id, "skipped (exists)"
    if args.dry_run:  # decide before touching the filesystem, so a later real run is not skipped
        return run_id, "dry-run" + (" (would replace)" if run_dir.exists() else "")
    rerun = None
    if run_dir.exists():
        # keep a trace of what this run replaces, so corpus history can be derived from meta.json
        old_meta, old_score = read_json(run_dir / "meta.json", {}) or {}, read_json(run_dir / "score.json", {}) or {}
        rerun = {"previous_started": old_meta.get("started"), "previous_invalid_reason": old_score.get("invalid_reason"),
                 "previous_incomplete": not (run_dir / "meta.json").exists()}
        shutil.rmtree(run_dir)
    run_dir.mkdir(parents=True)
    ws = run_dir / "workspace"
    codex_home = run_dir / "codex_home"
    seed_workspace(ws, prompt.get("seed", "seed"))
    if sub["harness"] == "codex":
        make_codex_home(codex_home, sub["model"], ws)
    text = prompt["prompt"]
    if delivery == "inline":
        text = inline_prompt(prompt["skill"], text)
    elif prompt_skills(prompt):  # baseline prompts run with no skill installed
        install_skills(ws, codex_home, sub["harness"], delivery, prompt_skills(prompt))
    env = {k: v for k, v in os.environ.items() if not k.startswith("CLAUDE")}
    env["CODEX_HOME"] = str(codex_home)
    if sub["harness"] == "claude-code":
        cmd, stdin = claude_cmd(sub["model"], text, args.max_turns), None
    else:
        cmd, stdin = codex_cmd(sub["model"], ws, run_dir), text
    meta = {"run_id": run_id, "subject": subject, "harness": sub["harness"], "model": sub["model"],
            "delivery": delivery, "prompt": prompt, "rep": rep, "cmd": cmd, "started": time.time(), "rerun": rerun}
    t0, m0 = time.time(), time.monotonic()
    try:
        proc = subprocess.run(cmd, cwd=ws, env=env, input=stdin, capture_output=True, text=True,
                              timeout=args.timeout)
        meta.update(exit_code=proc.returncode, timed_out=False)
        (run_dir / "stdout.jsonl").write_text(proc.stdout)
        (run_dir / "stderr.txt").write_text(proc.stderr)
    except subprocess.TimeoutExpired as e:
        meta.update(exit_code=None, timed_out=True)
        (run_dir / "stdout.jsonl").write_text(e.stdout or "")
        (run_dir / "stderr.txt").write_text(e.stderr or "")
    meta["wall_s"] = round(time.time() - t0, 2)
    # monotonic time stops while the machine sleeps; the gap to wall time shows an interrupted run
    meta["active_s"] = round(time.monotonic() - m0, 2)
    meta["timeout"] = args.timeout
    diff = subprocess.run(["git", "status", "--porcelain"], cwd=ws, capture_output=True, text=True)
    meta["git_status"] = diff.stdout
    (run_dir / "meta.json").write_text(json.dumps(meta, indent=2))
    return run_id, f"exit={meta['exit_code']} wall={meta['wall_s']}s"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subjects", nargs="+", default=list(SUBJECTS))
    ap.add_argument("--delivery", nargs="+", default=DELIVERIES)
    ap.add_argument("--prompts", nargs="+", help="prompt ids; default all")
    ap.add_argument("--study", choices=["branch", "work", "gate"])
    ap.add_argument("--reps", type=int, default=2)
    ap.add_argument("--parallel", type=int, default=3)
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--max-turns", type=int, default=30)
    ap.add_argument("--force", action="store_true", help="rerun cells that already exist")
    ap.add_argument("--rerun-invalid", action="store_true", help="rerun cells whose score.json marks them invalid")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    prompts = [p for p in load_prompts(args.study) if not args.prompts or p["id"] in args.prompts]
    # delivery is meaningless without a skill, so baseline prompts get a single "none" cell;
    # a selection set cannot be delivered inline (DESIGN.md, Delivery conditions), so those cells are dropped
    def deliveries(p):
        if not prompt_skills(p): return ["none"]
        return [d for d in args.delivery if not (p["kind"] == "selection" and d == "inline")]
    cells = [(s, d, p, r) for s in args.subjects for p in prompts
             for d in deliveries(p) for r in range(1, args.reps + 1)]
    print(f"{len(cells)} cells", file=sys.stderr)
    RUNS.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=args.parallel) as ex:
        for run_id, status in ex.map(lambda c: do_run(c, args), cells):
            print(f"{run_id}: {status}", flush=True)


if __name__ == "__main__":
    main()
