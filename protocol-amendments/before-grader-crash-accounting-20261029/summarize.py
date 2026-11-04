import csv
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from attest_trial import reviewed_scoring_interruption

ROOT = Path(__file__).resolve().parent


def summarize_rows(rows):
    summary = {}
    for condition in sorted({row['condition'] for row in rows}):
        selected = [r for r in rows if r['condition'] == condition]
        scored = [r for r in selected if r['status'] == 'scored']
        summary[condition] = {
            'planned':len(selected), 'scored':len(scored),
            'passed':sum(r['reward'] == 1 for r in scored),
            'scored_with_verified_isolation':sum(r['isolation_audit_passed'] is True for r in scored),
            'scored_with_provider_interruption':sum(r['provider_interruption'] is True for r in scored),
            'unscored_errors':sum(r['status'] == 'unscored_error' for r in selected),
            'pending':sum(r['status'] == 'pending' for r in selected),
            'running':sum(r['status'] == 'running' for r in selected),
            'infrastructure_hold':sum(r['status'] == 'infrastructure_hold' for r in selected),
            'awaiting_grader_recovery':sum(r['status'] == 'awaiting_grader_recovery' for r in selected),
        }
    return summary


def seconds(timing):
    if not timing or not timing.get("started_at") or not timing.get("finished_at"):
        return None
    return (
        datetime.fromisoformat(timing["finished_at"])
        - datetime.fromisoformat(timing["started_at"])
    ).total_seconds()


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from strings(item)


def extract_trace(trial_dir, expected_prompt):
    calls = []
    messages = []
    outputs = {}
    contexts = []
    prompt_recorded = False
    usage = None
    session_files = sorted((trial_dir / "agent").rglob("rollout-*.jsonl"))
    for path in session_files:
        for line_number, line in enumerate(path.read_text().splitlines(), 1):
            item = json.loads(line)
            payload = item.get("payload", {})
            if item.get("type") == "session_meta":
                prompt_recorded |= any(s.strip() == expected_prompt.strip() for s in strings(payload))
            elif item.get("type") == "turn_context":
                contexts.append({k: payload.get(k) for k in ("model", "effort", "reasoning_effort", "cwd")})
            elif item.get("type") == "event_msg" and payload.get("type") == "token_count":
                candidate = (payload.get("info") or {}).get("total_token_usage")
                if candidate:
                    usage = candidate
            elif item.get("type") == "response_item":
                kind = payload.get("type")
                location = f"{path.relative_to(ROOT)}:{line_number}"
                if kind in ("function_call", "custom_tool_call"):
                    raw = payload.get("arguments", payload.get("input", ""))
                    if kind == "function_call":
                        args = json.loads(raw) if isinstance(raw, str) else raw
                    else:
                        args = raw
                    command = None
                    if isinstance(args, dict):
                        command = args.get("cmd", args.get("command"))
                    calls.append({
                        "name": payload.get("name"), "call_id": payload.get("call_id"),
                        "arguments": args, "command": command,
                        "timestamp": item.get("timestamp"), "source": location,
                    })
                elif kind in ("function_call_output", "custom_tool_call_output"):
                    outputs[payload.get("call_id")] = payload.get("output")
                elif kind == "message" and payload.get("role") == "assistant":
                    if payload.get("channel") != "analysis":
                        messages.append({
                            "channel": payload.get("channel"),
                            "phase": payload.get("phase"),
                            "text": "\n".join(c.get("text", "") for c in payload.get("content", []) if isinstance(c, dict)),
                            "source": location,
                        })
    for call in calls:
        call["output"] = outputs.get(call["call_id"])
    return {
        "session_files": [str(p.relative_to(ROOT)) for p in session_files],
        "expected_prompt_recorded": prompt_recorded,
        "turn_contexts": contexts,
        "last_total_token_usage": usage,
        "tool_counts": dict(Counter(c["name"] for c in calls)),
        "calls": calls,
        "visible_messages": messages,
    }


def main():
    plan = json.loads((ROOT / "experiment-plan.json").read_text())
    task_info = {t["name"]: t for t in plan["tasks"]}
    rows = []
    review_dir = ROOT / "review"
    review_dir.mkdir(exist_ok=True)
    for item in plan["schedule"]:
        name = f"{item['task']}--{item['condition']}--r{item['repeat']}"
        job_dir = ROOT / "jobs" / name
        paths = sorted(job_dir.glob("*/result.json"))
        row = {**item, "language_metadata": task_info[item["task"]]["language"], "job": name, "status": "pending"}
        if len(paths) > 1:
            raise RuntimeError(f"Expected one independent trial in {name}, found {len(paths)}")
        if paths:
            path = paths[0]
            raw = json.loads(path.read_text())
            if not raw.get("finished_at"):
                row["status"] = "running"
                rows.append(row)
                continue
            trace = extract_trace(path.parent, (ROOT / "prompts" / f"{item['condition']}.md").read_text())
            trace_path = review_dir / f"{name}.json"
            serialized_trace = json.dumps(trace, indent=2)
            serialized_trace = re.sub(r'http://agent:[A-Za-z0-9_-]+@pier-egress-proxy', 'http://agent:[redacted]@pier-egress-proxy', serialized_trace)
            trace_path.write_text(serialized_trace + "\n")
            usage = trace["last_total_token_usage"] or {}
            agent = raw.get("agent_result") or {}
            audit_path = path.parent / "agent" / "isolation-audit.json"
            audit = json.loads(audit_path.read_text()) if audit_path.exists() else None
            attestation_path = path.parent / "agent" / "attestation.json"
            attestation = json.loads(attestation_path.read_text()) if attestation_path.exists() else None
            scores = (raw.get("verifier_result") or {}).get("rewards") or {}
            exception = (raw.get("exception_info") or {}).get("exception_type")
            interruption = reviewed_scoring_interruption(path.parent)
            valid = (scores.get("reward") in [0, 1]
                     and exception in [None, "AgentTimeoutError"]
                     and audit is not None and audit["passed"]
                     and attestation is not None and attestation["passed"])
            row.update({
                "status": "scored" if valid else "unscored_error",
                "reward": scores.get("reward"),
                **{key: scores.get(key) for key in ["f2p_total", "f2p_passed", "p2p_total", "p2p_passed", "partial"]},
                "exception": exception,
                "native_attestation_passed": attestation["passed"] if attestation else None,
                "native_identity_attestation_passed": attestation.get("identity_passed", attestation["passed"]) if attestation else None,
                "provider_interruption": interruption,
                "completion_state": "provider_capacity_interrupted" if interruption else "official_timeout" if exception == "AgentTimeoutError" else "completed",
                "agent_seconds": seconds(raw.get("agent_execution")),
                "setup_seconds": seconds(raw.get("agent_setup")),
                "verifier_seconds": seconds(raw.get("verifier")),
                "input_tokens": usage.get("input_tokens", agent.get("n_input_tokens")),
                "cached_input_tokens": usage.get("cached_input_tokens", agent.get("n_cache_tokens")),
                "output_tokens": usage.get("output_tokens", agent.get("n_output_tokens")),
                "reasoning_output_tokens": usage.get("reasoning_output_tokens"),
                "tool_calls": len(trace["calls"]),
                "visible_messages": len(trace["visible_messages"]),
                "expected_prompt_recorded": trace["expected_prompt_recorded"],
                "isolation_audit_passed": audit["passed"] if audit else None,
                "enabled_skills": ",".join(s["name"] for s in audit["skills"] if s["enabled"]) if audit else None,
                "isolation_audit_path": str(audit_path.relative_to(ROOT)) if audit else None,
                "result_path": str(path.relative_to(ROOT)),
                "review_path": str(trace_path.relative_to(ROOT)),
            })
        elif (job_dir / "operator-stop.json").exists():
            row["operator_stop_marker"] = True
        elif (job_dir / "operator-infrastructure-hold.json").exists():
            row['status'] = 'infrastructure_hold'
            row['infrastructure_hold_marker'] = True
        elif job_dir.exists():
            row["status"] = "running"
        rows.append(row)
    (ROOT / "results.json").write_text(json.dumps(rows, indent=2) + "\n")
    fields = list(dict.fromkeys(key for row in rows for key in row))
    with (ROOT / "results.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    summary = summarize_rows(rows)
    (ROOT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary,indent=2))


if __name__ == "__main__":
    main()
