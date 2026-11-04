import asyncio
from datetime import datetime, timezone
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess

from pier.models.trial.config import TrialConfig
from pier.trial.trial import Trial

from attest_trial import attest_trial
from run_experiment import ROOT, PLAN, SOCKET, write_json
from verifier_recovery import reviewed_verifier_recovery

JOB = 'abs-module-cache-flags--bundled--r2'
TRIAL = 'abs-module-cache-flags__jM59Ykt'


async def main():
    if os.environ.get('DOCKER_HOST') != SOCKET:
        raise RuntimeError('Dedicated Docker socket required')
    previous = Path(PLAN['runtime_previous_root'])
    lock = (previous / 'runner.lock').open('a')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    processes = subprocess.run(['pgrep', '-fl', 'run_batch[.]py'], capture_output=True, text=True)
    if processes.returncode not in [0, 1] or processes.stdout.strip():
        raise RuntimeError('Existing worker must not be duplicated')
    if subprocess.check_output(['docker', 'ps', '-q'], text=True).strip():
        raise RuntimeError('Dedicated containers remain active')
    if not (previous / 'jobs/ink-grid-box-layout--override--r1/operator-stop.json').is_file():
        raise RuntimeError('Original operator stop barrier missing')
    original = ROOT / 'jobs' / JOB / TRIAL
    raw_bytes = (original / 'result.json').read_bytes()
    raw = json.loads(raw_bytes)
    if (raw.get('exception_info') or {}).get('exception_type') != 'RuntimeError' or raw.get('verifier_result') is not None:
        raise RuntimeError('Unexpected original result')
    if 'load metadata for public.ecr.aws' not in raw['exception_info']['exception_message'] or 'dial tcp 198.18.0.59:443: i/o timeout' not in raw['exception_info']['exception_message']:
        raise RuntimeError('Expected reviewed registry connection interruption')
    if any((original / 'verifier').iterdir()):
        raise RuntimeError('Existing verifier output requires inspection')
    archive = ROOT / 'infrastructure/attempts' / (JOB + '--grader-network-20261030T040549Z')
    shutil.copytree(original.parent, archive)
    attestation = attest_trial(original, ROOT / PLAN['prompt_files']['bundled'])
    if not attestation['passed'] or not attestation['normal_turn_completed']:
        raise RuntimeError('Original model did not complete normally')
    if not json.loads((original / 'agent/isolation-audit.json').read_text())['passed']:
        raise RuntimeError('Original isolation failed')
    recovery_parent = ROOT / 'recoveries' / JOB
    recovery_parent.mkdir(parents=True, exist_ok=False)
    write_json(recovery_parent / 'started.json', {
        'started_at': datetime.now(timezone.utc).isoformat(), 'pid': os.getpid(),
        'original_trial': TRIAL, 'original_archive': str(archive.relative_to(ROOT)),
        'additional_model_executions': 0, 'reason': 'Registry connection timeout before official grader execution',
    })
    image = 'public.ecr.aws/d3j8x8q7/swe-bench-202605:kh75679ajj3b8dtd7se3h7z0a1833y6r-v1.1'
    with (recovery_parent / 'image-pull.log').open('w') as log:
        pull = subprocess.run(['docker', 'pull', '--platform', 'linux/amd64', image], stdout=log, stderr=subprocess.STDOUT)
    write_json(recovery_parent / 'image-pull.json', {'checked_at': datetime.now(timezone.utc).isoformat(), 'image': image, 'exit_code': pull.returncode})
    pull.check_returncode()
    config = TrialConfig.model_validate_json((original / 'config.json').read_text())
    config.trials_dir = recovery_parent
    config.trial_name = TRIAL + '-grader-recovery'
    trial = await Trial.create(config)
    write_json(trial.trial_dir / 'config.json', config.model_dump(mode='json'))
    shutil.copytree(original / 'artifacts', trial.trial_dir / 'artifacts', dirs_exist_ok=True)
    started = datetime.now(timezone.utc)
    print('Running only the native separate verifier on the retained patch', flush=True)
    try:
        result = await asyncio.wait_for(
            trial._verify_once(step_cfg=None, artifacts_dir=trial.trial_dir / 'artifacts'),
            timeout=trial._verifier_timeout_sec,
        )
    finally:
        trial._close_logger_handler()
    finished = datetime.now(timezone.utc)
    write_json(trial.trial_dir / 'verification-result.json', {
        'started_at': started.isoformat(), 'finished_at': finished.isoformat(),
        'verifier_result': result.model_dump(mode='json'),
    })
    grade = json.loads((trial.trial_dir / 'verifier/reward.json').read_text())
    if result.rewards != grade or grade.get('reward') not in [0, 1]:
        raise RuntimeError('Official grade mismatch')
    if (trial.trial_dir / 'verifier/test-stdout.txt').read_text().count('===== grade =====') != 1:
        raise RuntimeError('Expected exactly one official grading execution')
    if (original / 'result.json').read_bytes() != raw_bytes:
        raise RuntimeError('Original result changed')
    (original / 'verifier').rmdir()
    shutil.copytree(trial.trial_dir / 'verifier', original / 'verifier')
    receipt = {
        'passed': True, 'classification': 'verifier_registry_io_before_execution',
        'trial': TRIAL, 'job': JOB, 'model_executions': 1, 'verifier_executions': 1,
        'verifier_environment_start_attempts': 2, 'additional_model_executions': 0,
        'original_result_preserved': True, 'original_patch_preserved': True,
        'original_archive': str(archive.relative_to(ROOT)),
        'recovery_directory': str(trial.trial_dir.relative_to(ROOT)),
        'recovery_seconds': (finished - started).total_seconds(),
        'recovered_at': finished.isoformat(), 'reward': grade['reward'],
    }
    write_json(original / 'verifier-recovery.json', receipt)
    reviewed_verifier_recovery(original)
    print(json.dumps(receipt), flush=True)


if __name__ == '__main__':
    asyncio.run(main())
