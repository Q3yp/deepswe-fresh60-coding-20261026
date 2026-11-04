import json
from pathlib import Path


def reviewed_resource_limit_failure(directory):
    receipt_path = directory / 'agent/resource-limit-review.json'
    if not receipt_path.exists():
        return None
    receipt = json.loads(receipt_path.read_text())
    root = Path(__file__).resolve().parent
    raw = json.loads((directory / 'result.json').read_text())
    grade = json.loads((directory / 'verifier/reward.json').read_text())
    kernel = json.loads((root / receipt['kernel_evidence']).read_text())
    kernel_text = '\n'.join(c['stdout'] for c in kernel['checks'] if c['code'] == 0)
    archive = root / receipt['original_archive'] / directory.name
    valid = (
        receipt['classification'] == 'agent_container_memory_limit'
        and receipt['trial'] == directory.name and receipt['job'] == directory.parent.name
        and receipt['model_executions'] == receipt['verifier_executions'] == 1
        and receipt['additional_model_executions'] == 0
        and receipt['limit_mb'] == json.loads((root / 'experiment-plan.json').read_text())['memory_mb']
        and f"memory: usage {receipt['limit_mb'] * 1024}kB, limit {receipt['limit_mb'] * 1024}kB" in kernel_text
        and any('oom-kill:constraint=CONSTRAINT_MEMCG' in line
                and f"task_memcg=/docker/{receipt['container_id']}" in line
                and 'task=codex,' in line for line in kernel_text.splitlines())
        and (raw.get('exception_info') or {}).get('exception_type') == 'NonZeroAgentExitCodeError'
        and 'Command failed (exit 137)' in raw['exception_info']['exception_message']
        and raw['agent_execution']['finished_at'] == receipt['agent_finished_at']
        and raw.get('finished_at')
        and (raw.get('verifier_result') or {}).get('rewards') == grade
        and grade['reward'] == 0
        and (directory / 'verifier/test-stdout.txt').read_text().count('===== grade =====') == 1
        and all((archive / name).read_bytes() == (directory / name).read_bytes()
                for name in ['result.json', 'artifacts/model.patch', 'verifier/reward.json'])
    )
    if not valid:
        raise RuntimeError(f'Resource-limit review does not match retained evidence: {directory}')
    return receipt


def reviewed_scoring_interruption(directory):
    receipt_path = directory / 'agent/interruption-review.json'
    if not receipt_path.exists():
        return False
    receipt = json.loads(receipt_path.read_text())
    raw = json.loads((directory / 'result.json').read_text())
    grade = json.loads((directory / 'verifier/reward.json').read_text())
    events = []
    for line in (directory / 'agent/codex.txt').read_text().splitlines():
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    valid = (
        receipt['trial'] == directory.name
        and receipt['classification'] in ('provider_capacity_after_commit', 'provider_capacity_before_commit')
        and (receipt['classification'] != 'provider_capacity_before_commit'
             or ((directory / 'artifacts/model.patch').stat().st_size == 0 and grade['reward'] == 0))
        and receipt['provider_message'] == 'Selected model is at capacity. Please try a different model.'
        and receipt['model_executions'] == receipt['verifier_executions'] == 1
        and (raw.get('exception_info') or {}).get('exception_type') == 'NonZeroAgentExitCodeError'
        and events[-1] == {'type': 'turn.failed', 'error': {'message': receipt['provider_message']}}
        and sum(e.get('type') == 'thread.started' for e in events) == 1
        and sum(e.get('type') == 'turn.started' for e in events) == 1
        and not any(e.get('type') == 'turn.completed' for e in events)
        and (directory / 'verifier/test-stdout.txt').read_text().count('===== grade =====') == 1
        and grade['reward'] in [0, 1]
        and raw.get('finished_at')
        and (raw.get('verifier_result') or {}).get('rewards') == grade
    )
    if not valid:
        raise RuntimeError(f'Interruption review does not match retained native evidence: {directory}')
    return True


def attest_trial(directory, prompt_path, timed_out=False):
    sessions = list((directory / 'agent/sessions').rglob('*.jsonl'))
    events = []
    for path in sessions:
        for line in path.read_text().splitlines():
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                if not timed_out:
                    raise
    metadata = [e['payload'] for e in events if e.get('type') == 'session_meta']
    turns = [e['payload'] for e in events if e.get('type') == 'turn_context']
    expected_prompt = Path(prompt_path).read_text().strip()
    cli_events = []
    for line in (directory / 'agent/codex.txt').read_text().splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(event, dict):
            cli_events.append(event)
    usage = [e['payload'].get('info') for e in events
             if e.get('type') == 'event_msg' and e['payload'].get('type') == 'token_count']
    usage = [u for u in usage if u]
    checks = {
        'native_session_exists': bool(metadata),
        'version_0_163_0': bool(metadata) and all(m.get('cli_version') == '0.163.0' for m in metadata),
        'exact_frozen_prompt': bool(metadata) and all(
            (m.get('base_instructions') or {}).get('text', '').strip() == expected_prompt
            for m in metadata),
        'astra_xhigh': bool(turns) and all(t.get('model') == 'gpt-6-astra' and t.get('effort') == 'xhigh' for t in turns),
        'model_produced_tokens': bool(usage) and (usage[-1].get('total_token_usage') or {}).get('output_tokens', 0) > 0,
        'completed_or_official_timeout': timed_out or any(e.get('type') == 'turn.completed' for e in cli_events),
    }
    identity_passed = all(value for key, value in checks.items()
                          if key != 'completed_or_official_timeout')
    interruption = reviewed_scoring_interruption(directory)
    report = {'passed': all(checks.values()), 'checks': checks,
              'identity_passed': identity_passed,
              'normal_turn_completed': any(e.get('type') == 'turn.completed' for e in cli_events),
              'reviewed_provider_interruption': interruption,
              'scoring_eligible': all(checks.values()),
              'session_count': len(metadata), 'official_timeout': timed_out,
              'cli_statuses': [e.get('type') for e in cli_events
                               if e.get('type') in ['thread.started', 'turn.completed', 'turn.failed', 'error']]}
    (directory / 'agent/attestation.json').write_text(json.dumps(report, indent=2) + '\n')
    return report
