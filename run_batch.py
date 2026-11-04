import asyncio
from datetime import datetime, timezone
import fcntl
import json
import os
from pathlib import Path
import subprocess
import sys

from attest_trial import attest_trial, reviewed_scoring_interruption, reviewed_resource_limit_failure
from verifier_recovery import reviewed_verifier_recovery
from run_experiment import ROOT, PLAN, SOCKET, prune_task_cache, record, run_job, write_json


def inspect_completed(name, condition):
    paths = list((ROOT / 'jobs' / name).glob('*/result.json'))
    if len(paths) != 1:
        raise RuntimeError(f'Expected exactly one retained trial: {name}')
    trial = paths[0].parent
    raw = json.loads(paths[0].read_text())
    if not raw.get('finished_at'):
        raise RuntimeError(f'Trial remains unfinished: {name}')
    grade = json.loads((trial / 'verifier/reward.json').read_text())
    exception = (raw.get('exception_info') or {}).get('exception_type')
    interruption = reviewed_scoring_interruption(trial)
    recovery = reviewed_verifier_recovery(trial)
    resource_failure = reviewed_resource_limit_failure(trial)
    if exception not in [None, 'AgentTimeoutError'] and not recovery and not resource_failure:
        raise RuntimeError(f'Retain infrastructure error for inspection: {name}: {exception}')
    elif not recovery and (raw.get('verifier_result') or {}).get('rewards', {}).get('reward') != grade['reward']:
        raise RuntimeError(f'Native result and official reward disagree: {name}')
    if grade['reward'] not in [0, 1]:
        raise RuntimeError(f'Unscored trial requires inspection: {name}')
    if not json.loads((trial / 'agent/isolation-audit.json').read_text())['passed']:
        raise RuntimeError(f'Native isolation audit failed: {name}')
    attestation_path = trial / 'agent/attestation.json'
    if attestation_path.exists():
        attestation = json.loads(attestation_path.read_text())
    else:
        attestation = attest_trial(trial, ROOT / PLAN['prompt_files'][condition], timed_out=exception == 'AgentTimeoutError')
    if not (attestation['passed'] or (resource_failure and attestation['identity_passed'])):
        raise RuntimeError(f'Native prompt/model attestation failed: {name}')
    return {'job': name, 'reward': grade['reward'], 'imported': name in PLAN['reused_jobs'],
            'provider_interruption': interruption, 'exception': exception,
            'verifier_recovered': bool(recovery),
            'model_resource_limit_failure': bool(resource_failure),
            'f2p_passed': grade['f2p_passed'], 'f2p_total': grade['f2p_total'],
            'p2p_passed': grade['p2p_passed'], 'p2p_total': grade['p2p_total']}


async def main():
    previous = Path(PLAN['runtime_previous_root'])
    if os.environ.get('DOCKER_HOST') != SOCKET:
        raise RuntimeError('The dedicated Docker socket is required')
    lock = (previous / 'runner.lock').open('a')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    if subprocess.check_output(['docker', 'ps', '-q'], text=True).strip():
        raise RuntimeError('Dedicated Docker has active containers; do not duplicate work')
    if not (previous / 'jobs/ink-grid-box-layout--override--r1/operator-stop.json').exists():
        raise RuntimeError('Original study stop barrier is missing')
    for name in ['probe-status.json', 'preflight-status.json']:
        if not json.loads((previous / name).read_text())['passed']:
            raise RuntimeError(f'Established calibration unavailable: {name}')
    schedule = PLAN['schedule']
    names = [f"{x['task']}--{x['condition']}--r{x['repeat']}" for x in schedule]
    if len(names) != 240 or len(set(names)) != 240 or PLAN['reused_jobs'] or PLAN['additional_model_trials'] != 240:
        raise RuntimeError('This fresh comparison authorizes240 new slots and no imported scores')
    vm_plan = subprocess.check_output(
        ['colima', 'ssh', '--profile', 'codex-deepswe', '--', 'cat', str(ROOT / 'experiment-plan.json')], text=True
    )
    if json.loads(vm_plan) != PLAN:
        raise RuntimeError('Host and VM do not see the same batch directory')
    record('shared_directory_verified', root=str(ROOT))
    write_json(ROOT / 'runner-process.json', {
        'pid': os.getpid(), 'started_at': datetime.now(timezone.utc).isoformat(),
        'phase': 'fresh60-bundled-coding', 'planned_trials': 240, 'new_trials': 240,
    })
    os.environ['CODEX_AUTH_JSON_PATH'] = str(ROOT / '.secrets/auth.json')
    os.environ['CODEX_FORCE_AUTH_JSON'] = 'true'
    completed = []
    for index, (item, name) in enumerate(zip(schedule, names)):
        reused = (ROOT / 'jobs' / name / 'result.json').exists()
        if not reused:
            await run_job(name, item['task'], {
                'import_path': 'prompt_agent:PromptCodex',
                'model_name': 'openai/gpt-6-astra', 'override_setup_timeout_sec': 900,
                'kwargs': {
                    'version': PLAN['codex_version'], 'reasoning_effort': 'xhigh',
                    'config_toml_file': str(ROOT / 'codex-config.toml'),
                    'prompt_template_path': str(ROOT / 'instruction.jinja'),
                    'prompt_path': str(ROOT / PLAN['prompt_files'][item['condition']]),
                    'conveying_path': str(ROOT / 'skills/conveying/SKILL.md'),
                },
            })
        outcome = inspect_completed(name, item['condition'])
        completed.append(outcome)
        record('verified_existing_score' if reused else 'verified_new_score', **outcome)
        write_json(ROOT / 'batch-status.json', {
            'updated_at': datetime.now(timezone.utc).isoformat(), 'planned': 240,
            'scored': len(completed), 'passed': sum(x['reward'] for x in completed),
            'completed': completed,
        })
        if not reused and (index + 1 == len(schedule) or schedule[index + 1]['task'] != item['task']):
            prune_task_cache()
    subprocess.run([sys.executable, str(ROOT / 'summarize.py')], check=True)
    write_json(ROOT / 'experiment-status.json', {
        'finished': True, 'finished_at': datetime.now(timezone.utc).isoformat(),
        'planned': 240, 'scored': len(completed), 'passed': sum(x['reward'] for x in completed),
        'new_model_trials': 240, 'reused_trials': 0,
    })
    record('batch_finished', scored=len(completed), passed=sum(x['reward'] for x in completed))
    (ROOT / '.secrets/auth.json').unlink(missing_ok=True)
    subprocess.run(['colima', 'stop', '--profile', 'codex-deepswe'], check=True)
    write_json(ROOT / 'cleanup-status.json', {
        'finished_at': datetime.now(timezone.utc).isoformat(),
        'copied_auth_removed': True, 'dedicated_vm_stopped': True, 'vm_disk_retained': True,
    })


if __name__ == '__main__':
    asyncio.run(main())
