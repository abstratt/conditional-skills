#!/usr/bin/env python3
"""Aggregate score.json and judge.json into results/summary.md and results/runs.csv."""
import csv, json, re, sys, time
from collections import defaultdict
from statistics import mean
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from common import *
import claims as claims_mod


def pct(xs):
    xs = [x for x in xs if x is not None]
    return f"{100 * mean(xs):.0f}% (n={len(xs)})" if xs else "-"


def avg(xs, fmt="{:.2f}"):
    xs = [x for x in xs if x is not None]
    return fmt.format(mean(xs)) if xs else "-"


def main():
    rows = []
    for d in run_dirs():
        s = read_json(d / "score.json")
        if s:
            s["judge"] = read_json(d / "judge.json", {}) or {}
            s["meta"] = read_json(d / "meta.json", {}) or {}
            rows.append(s)
    if not rows:
        print("no scored runs"); return
    # invalid runs (infrastructure failures) are excluded everywhere and listed; see DESIGN.md, Run validity
    invalid = [r for r in rows if r.get("valid") is False]
    rows = [r for r in rows if r.get("valid") is not False]
    incomplete = sorted(d.name for d in RUNS.iterdir() if d.is_dir() and not (d / "meta.json").exists()) if RUNS.exists() else []
    RESULTS.mkdir(exist_ok=True)
    cols = ["run_id", "subject", "delivery", "study", "prompt_id", "skill", "rep",
            "triggered", "outcome_ok", "cost_usd", "tokens_in", "tokens_out", "tool_invocations", "turns", "wall_s", "timing_valid"]
    with open(RESULTS / "runs.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols + ["format_adherence", "scope_discipline", "honesty"], lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({**{c: r.get(c) for c in cols}, **{k: r["judge"].get(k) for k in ("format_adherence", "scope_discipline", "honesty")}})
    groups = defaultdict(list)
    for r in rows:
        groups[(r["subject"], r["delivery"])].append(r)
    out = ["# Results summary", "", f"{len(rows)} valid scored runs.", ""]
    if invalid or incomplete:
        out += ["## Excluded runs", "",
                "Invalid runs failed for infrastructure reasons and are left out of every table below. "
                "Rerun them with `bin/run.py --rerun-invalid`; incomplete runs are redone by a plain rerun.", ""]
        out += [f"- `{r['run_id']}`: invalid, {r['invalid_reason']}" for r in invalid]
        out += [f"- `{n}`: incomplete, no meta.json" for n in incomplete]
        out += [""]
    out += ["## Skill loading precondition", "",
            "A branch can only run if the skill was loaded. Loading rate per subject and delivery, over model-conditional prompts only. "
            "`inline` puts the instructions in the prompt, so it cannot fail to load; its column only shows whether the trace line was written:", "",
            "| subject | delivery | loaded, Study 1 | loaded, Study 2 |", "|---|---|---|---|"]
    for (sub, dl), rs in sorted(groups.items()):
        if dl == "none": continue
        out.append(f"| {sub} | {dl} | {pct([r['triggered'] for r in rs if r['study'] == 'branch'])} | "
                   f"{pct([r['triggered'] for r in rs if r['study'] == 'work'])} |")
    out += [""]
    out += ["## Study 1: branch selection", "",
            "| subject | delivery | skill | stamp present | fields correct | all fields | branch matches truth | branch consistent | outcome ok |",
            "|---|---|---|---|---|---|---|---|---|"]
    for (sub, dl), rs in sorted(groups.items()):
        for skill in ("vendor-stamp", "harness-stamp", "tier-stamp"):
            b = [r for r in rs if r["skill"] == skill]
            if not b: continue
            fc = sum(r["fields_correct"] for r in b); ft = sum(r["fields_total"] for r in b)
            out.append(f"| {sub} | {dl} | {skill} | {pct([r['stamp_present'] for r in b])} | {fc}/{ft} | "
                       f"{pct([r['all_fields_correct'] for r in b])} | {pct([r['branch_matches_truth'] for r in b])} | "
                       f"{pct([r['branch_consistent'] for r in b])} | {pct([r['outcome_ok'] for r in b])} |")
    out += ["", "Field-level detail:", ""]
    fields = defaultdict(list)
    for r in rows:
        if r["study"] == "branch":
            for k, v in r.get("fields", {}).items():
                fields[(r["subject"], r["delivery"], k)].append(v)
    out += ["| subject | delivery | field | correct |", "|---|---|---|---|"]
    for (sub, dl, k), vs in sorted(fields.items()):
        out.append(f"| {sub} | {dl} | {k} | {pct(vs)} |")
    work = [r for r in rows if r["study"] == "work"]
    if work:
        out += ["## Study 2: branches that change the work", ""]
        for skill in ("tiered-feature", "tiered-guidance"):
            if not any(r["skill"] == skill for r in work): continue
            out += [f"### {skill}", "",
                    "| subject | delivery | triggered | feature works | tests pass | reported tier = truth | work = reported | work = truth | mean tests | outcome ok |",
                    "|---|---|---|---|---|---|---|---|---|---|"]
            for (sub, dl), rs in sorted(groups.items()):
                t = [r for r in rs if r["skill"] == skill]
                if not t: continue
                out.append(f"| {sub} | {dl} | {pct([r['triggered'] for r in t])} | {pct([r['feature_ok'] for r in t])} | {pct([r['tests_pass'] for r in t])} | "
                           f"{pct([r['report_matches_truth'] for r in t])} | {pct([r['work_matches_report'] for r in t])} | "
                           f"{pct([r['work_matches_truth'] for r in t])} | {avg([r['n_tests'] for r in t], '{:.1f}')} | {pct([r['outcome_ok'] for r in t])} |")
            out += [""]
        out += ["Tier reported when it is free (Study 1), when a lower tier saves work (tiered-feature) and when a higher tier saves work (tiered-guidance):", "",
                "| subject | Study 1 tiers | tiered-feature tiers | tiered-guidance tiers |", "|---|---|---|---|"]
        from collections import Counter
        for sub in sorted({r["subject"] for r in rows}):
            b = Counter(r["stamp"].get("tier") for r in rows if r["skill"] == "tier-stamp" and r["subject"] == sub)
            c = Counter(r["reported_tier"] for r in rows if r["skill"] == "tiered-feature" and r["subject"] == sub)
            g = Counter(r["reported_tier"] for r in rows if r["skill"] == "tiered-guidance" and r["subject"] == sub)
            out.append(f"| {sub} | {dict(b)} | {dict(c)} | {dict(g) or '-'} |")
        base = [r for r in work if r["kind"] == "baseline" and r["prompt_id"].startswith("B") and not r["prompt_id"].startswith("BR")]
        if base:
            out += ["", "### No-skill baseline", "",
                    "The feature prompts with no skill installed, and the tier each skill's scoring would infer from that work:", "",
                    "| subject | runs | feature works | tests pass | docstring | mean tests | reads as tiered-feature | reads as tiered-guidance |",
                    "|---|---|---|---|---|---|---|---|"]
            for sub in sorted({r["subject"] for r in base}):
                t = [r for r in base if r["subject"] == sub]
                out.append(f"| {sub} | {len(t)} | {pct([r['feature_ok'] for r in t])} | {pct([r['tests_pass'] for r in t])} | "
                           f"{pct([r['docstring'] for r in t])} | {avg([r['n_tests'] for r in t], '{:.1f}')} | "
                           f"{dict(Counter(r['reads_as_feature'] for r in t))} | {dict(Counter(r['reads_as_guidance'] for r in t))} |")
        rbase = [r for r in work if r["prompt_id"].startswith("BR")]
        if rbase:
            out += ["", "### No-skill review baseline", "",
                    "The review prompts with no skill installed: does the model delegate unprompted, and does it find both planted bugs?", "",
                    "| subject | runs | delegation call seen | findings ok | src untouched |", "|---|---|---|---|---|"]
            for sub in sorted({r["subject"] for r in rbase}):
                t = [r for r in rbase if r["subject"] == sub]
                out.append(f"| {sub} | {len(t)} | {pct([r['delegated_call'] for r in t])} | {pct([r['findings_ok'] for r in t])} | "
                           f"{pct([r['src_untouched'] for r in t])} |")
        out += ["", "### tool-gated-review", "",
                "| subject | delivery | triggered | mode delegated | delegation call seen | mode = truth | mode consistent with calls | findings ok | src untouched | outcome ok |",
                "|---|---|---|---|---|---|---|---|---|---|"]
        for (sub, dl), rs in sorted(groups.items()):
            t = [r for r in rs if r["skill"] == "tool-gated-review"]
            if not t: continue
            out.append(f"| {sub} | {dl} | {pct([r['triggered'] for r in t])} | {pct([r['mode'] == 'delegated' for r in t])} | {pct([r['delegated_call'] for r in t])} | "
                       f"{pct([r['mode_matches_truth'] for r in t])} | {pct([r['mode_consistent'] for r in t])} | "
                       f"{pct([r['findings_ok'] for r in t])} | {pct([r['src_untouched'] for r in t])} | {pct([r['outcome_ok'] for r in t])} |")
        out += [""]
    out += ["", "## Adherence (LLM judge, 0-2)", "",
            "| subject | delivery | n judged | format | scope | honesty |", "|---|---|---|---|---|---|"]
    for (sub, dl), rs in sorted(groups.items()):
        j = [r["judge"] for r in rs if r["judge"].get("format_adherence") is not None]
        out.append(f"| {sub} | {dl} | {len(j)} | {avg([x['format_adherence'] for x in j])} | "
                   f"{avg([x['scope_discipline'] for x in j])} | {avg([x['honesty'] for x in j])} |")
    out += ["", "## Cost and latency (mean per run)", "",
            "| subject | delivery | cost USD | tokens in | tokens out | tool invocations | turns | wall s |", "|---|---|---|---|---|---|---|---|"]
    for (sub, dl), rs in sorted(groups.items()):
        out.append(f"| {sub} | {dl} | {avg([r['cost_usd'] for r in rs], '{:.3f}')} | {avg([r['tokens_in'] for r in rs], '{:.0f}')} | "
                   f"{avg([r['tokens_out'] for r in rs], '{:.0f}')} | {avg([r['tool_invocations'] for r in rs], '{:.1f}')} | {avg([r['turns'] for r in rs], '{:.1f}')} | "
                   f"{avg([r['wall_s'] for r in rs if r.get('timing_valid', True)], '{:.0f}')} |")
    slept = [r["run_id"] for r in rows if r.get("timing_valid") is False]
    out += ["", "Codex does not report USD cost or turns; tool invocations are the step count both harnesses expose. "
            "Tokens in include cached input for both harnesses."
            + (f" Wall time leaves out {len(slept)} runs whose timing is invalid: " + ", ".join(f"`{x}`" for x in slept) + "." if slept else ""), ""]
    fails = [r for r in rows if not r["trigger_correct"] or not r.get("outcome_ok")]
    if fails:
        out += ["## Runs that missed", ""]
        for r in fails:
            out.append(f"- `{r['run_id']}`: triggered={r['triggered']} (expected {r['expect_trigger']}), outcome_ok={r.get('outcome_ok')}, "
                       f"changed={r['changed_files']}" + (f", stamp={r['stamp']}" if r.get("stamp") else "")
                       + (f", reported={r.get('reported_tier')} implied={r.get('implied_tier')} feature_ok={r.get('feature_ok')}" if r["skill"] in ("tiered-feature", "tiered-guidance") else "")
                       + (f", mode={r.get('mode')} call={r.get('delegated_call')} findings={r.get('findings_ok')}" if r["skill"] == "tool-gated-review" else ""))
    (RESULTS / "summary.md").write_text("\n".join(out) + "\n")
    print("\n".join(out))
    write_claims(rows, invalid, incomplete)


def corpus_header(rows, invalid, incomplete):
    """The corpus a claims refresh was computed from, derived from run metadata (DESIGN.md, Report)."""
    by_day = defaultdict(int)
    reruns = []
    for r in rows:
        m = r["meta"]
        if m.get("started"):
            by_day[time.strftime("%Y-%m-%d", time.localtime(m["started"]))] += 1
        if m.get("rerun"):
            why = m["rerun"].get("previous_invalid_reason") or ("incomplete" if m["rerun"].get("previous_incomplete") else "forced")
            reruns.append(f"`{r['run_id']}` ({why})")
    lines = [f"- valid runs: {len(rows)} (skill runs {sum(1 for r in rows if r['kind'] != 'baseline')}, "
             f"baseline runs {sum(1 for r in rows if r['kind'] == 'baseline')})",
             "- batches by start date: " + ", ".join(f"{d}: {n}" for d, n in sorted(by_day.items())),
             "- reruns recorded in meta.json: " + (", ".join(reruns) if reruns else "none"),
             "- invalid runs (excluded): " + (", ".join(f"`{r['run_id']}`" for r in invalid) if invalid else "none"),
             "- incomplete run directories: " + (", ".join(f"`{n}`" for n in incomplete) if incomplete else "none"),
             "- timing-invalid runs (kept, excluded from wall-time means): " +
             (", ".join(f"`{r['run_id']}`" for r in rows if r.get("timing_valid") is False) or "none"),
             f"- fingerprint: `{claims_mod.fingerprint(rows)}`"]
    return lines


def check_findings(results, fp):
    """Flag FINDINGS.md paragraphs whose claims fail or changed status, unknown citations, and a stale fingerprint."""
    p = RESULTS / "FINDINGS.md"
    notes = []
    if not p.exists():
        return ["- no FINDINGS.md"]
    text = p.read_text()
    m = re.search(r"fingerprint:\s*`?([0-9a-f]{16})`?", text)
    if not m:
        notes.append("- FINDINGS.md has no fingerprint header, so it predates the claims mechanism")
    elif m.group(1) != fp:
        notes.append(f"- FINDINGS.md fingerprint `{m.group(1)}` differs from the current corpus `{fp}`: the file predates the data")
    by_id = {c["id"]: c for c in results}
    for i, para in enumerate(re.split(r"\n\s*\n", text)):
        ids = re.findall(r"\[claim:\s*([a-z0-9-]+)\]", para)
        for cid in ids:
            c = by_id.get(cid)
            head = " ".join(para.split())[:80]
            if not c:
                notes.append(f"- paragraph {i} cites unknown claim `{cid}`: \"{head}...\"")
            elif not c["holds"]:
                notes.append(f"- paragraph {i} cites `{cid}`, which fails: \"{head}...\"")
            elif c.get("status_changed"):
                notes.append(f"- paragraph {i} cites `{cid}`, whose status changed since the last refresh: \"{head}...\"")
    return notes or ["- nothing to revise"]


def write_claims(rows, invalid, incomplete):
    results = claims_mod.evaluate(rows)
    prev = read_json(RESULTS / "claims.json", {}) or {}
    for c in results:
        old = prev.get(c["id"])
        c["status_changed"] = bool(old) and old["holds"] != c["holds"]
        c["numbers_changed"] = bool(old) and old["holds"] == c["holds"] and old["values"] != c["values"]
        c["new"] = not old
    fp = claims_mod.fingerprint(rows)
    out = ["# Claims", "", "Checkable statements about the runs, re-evaluated on every refresh (see DESIGN.md, Report). "
           "Status is holds or fails; a claim is marked *status changed* or *numbers changed* against the last committed refresh.", "",
           "## Corpus", ""] + corpus_header(rows, invalid, incomplete) + [""]
    titles = {"branching": "Question 1: can a skill branch on model identity or capability?",
              "portability": "Question 2: is a single skill file portable?",
              "efficiency": "Question 3: what does a model-conditional skill cost?"}
    for q in ("branching", "portability", "efficiency"):
        out += [f"## {titles[q]}", ""]
        for c in results:
            if c["question"] != q: continue
            marks = []
            if c["new"]: marks.append("new")
            if c["status_changed"]: marks.append("status changed")
            if c["numbers_changed"]: marks.append("numbers changed")
            status = ("holds" if c["holds"] else "FAILS") + (f" ({', '.join(marks)})" if marks else "")
            out += [f'<a id="{c["id"]}"></a>', f"### `{c['id']}` — {status}, {c['kind']}", "", c["statement"], ""]
            rows_ = c["values"].get("rows") if isinstance(c["values"], dict) else None
            if rows_:
                out += ["| " + " | ".join(rows_[0]) + " |", "|" + "---|" * len(rows_[0])]
                out += ["| " + " | ".join(r) + " |" for r in rows_[1:]] + [""]
            for rid, ex in c["exhibits"]:
                out += [f"- exhibit `{rid}`: {ex}"]
            if c["exhibits"]: out += [""]
    out += ["## FINDINGS.md check", ""] + check_findings(results, fp) + [""]
    (RESULTS / "claims.md").write_text("\n".join(out) + "\n")
    (RESULTS / "claims.json").write_text(json.dumps(
        {c["id"]: {"holds": c["holds"], "values": c["values"], "question": c["question"], "kind": c["kind"]} for c in results},
        indent=2, sort_keys=True) + "\n")
    failing = [c["id"] for c in results if not c["holds"]]
    print(f"claims: {len(results)} evaluated, {len(failing)} failing" + (f": {', '.join(failing)}" if failing else ""), file=sys.stderr)


if __name__ == "__main__":
    main()
