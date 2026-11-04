import asyncio
from datetime import datetime, timezone
import fcntl
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

from pier.environments.docker.docker import DockerEnvironment
from pier.models.trial.config import TrialConfig
from pier.trial.trial import Trial

from run_experiment import ROOT, PLAN, SOCKET, write_json
from verifier_recovery import reviewed_verifier_recovery


class MongoGraderEnvironment(DockerEnvironment):
    @property
    def _docker_compose_paths(self):
        override = ROOT / 'infrastructure/eicrud-nofile-recovery.yaml'
        return [*super()._docker_compose_paths, override]

    async def start(self, force_build):
        if self.agent_install_spec is not None or self.environment_dir != ROOT / 'tasks/eicrud-keyset-pagination-cursor/tests':
            raise RuntimeError('This environment is restricted to the separate Eicrud verifier')
        await super().start(force_build)
        result = await self.exec('cat /proc/self/limits', user='root')
        write_json(self.trial_paths.trial_dir / 'limits-before.json', result.model_dump())
        if not re.search(r'Max open files\s+65536\s+524288', result.stdout or ''):
            raise RuntimeError('Expected repaired soft limit and unchanged hard limit')

    async def stop(self, delete):
        result = await self.exec(
            "cat /proc/self/limits; "
            "for p in $(pgrep -x mongod); do echo MONGO_PID=$p; cat /proc/$p/limits; "
            "ls /proc/$p/fd | wc -l; done; "
            "cat /sys/fs/cgroup/memory.events; df -h /data/db; "
            "test ! -f /var/log/mongod.log || cp /var/log/mongod.log /logs/verifier/mongod-recovery.log",
            user='root', timeout_sec=30,
        )
        write_json(self.trial_paths.trial_dir / 'database-after.json', result.model_dump())
        await super().stop(delete)


async def main():
    if os.environ.get('DOCKER_HOST') != SOCKET:
        raise RuntimeError('Dedicated socket required')
    previous = Path(PLAN['runtime_previous_root'])
    lock = (previous / 'runner.lock').open('a')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    processes = subprocess.run(['pgrep', '-fl', 'run_batch[.]py|docker compose.*build|docker-buildx build'], capture_output=True, text=True)
    if processes.returncode not in [0, 1] or processes.stdout.strip():
        raise RuntimeError('Worker or associated build is active')
    if subprocess.check_output(['docker', 'ps', '-q'], text=True).strip():
        raise RuntimeError('Dedicated containers active')
    if (ROOT / '.secrets/auth.json').exists():
        raise RuntimeError('Model credential must remain removed')
    if not (previous / 'jobs/ink-grid-box-layout--override--r1/operator-stop.json').is_file():
        raise RuntimeError('Original operator barrier missing')
    probe = json.loads((ROOT / 'infrastructure/eicrud-environment-limits-20261030.json').read_text())
    if probe['probe_exit'] or not re.search(r'Max open files\s+1024\s+524288', probe['stdout']):
        raise RuntimeError('Expected measured original resource limit')
    write_json(ROOT / 'infrastructure/eicrud-recovery-process.json', {
        'pid': os.getpid(), 'started_at': datetime.now(timezone.utc).isoformat(),
        'scope': 'Four same-patch separate official verifiers only; no model executions',
    })
    pending_path = ROOT / 'infrastructure/grader-recovery-status.json'
    pending = json.loads(pending_path.read_text())
    for job, status in pending['jobs'].items():
        if status['status'] != 'pending':
            continue
        if subprocess.check_output(['docker', 'ps', '-q'], text=True).strip():
            raise RuntimeError('Dedicated containers remain active between recoveries')
        original, = (ROOT / 'jobs' / job).glob('*/result.json')
        original = original.parent
        raw = json.loads((original / 'result.json').read_text())
        attestation = json.loads((original / 'agent/attestation.json').read_text())
        if raw['exception_info'] is not None or raw['verifier_result']['rewards']['reward'] != 0:
            raise RuntimeError('Unexpected original native result')
        if not attestation['passed'] or not attestation['normal_turn_completed']:
            raise RuntimeError('Original model completion was not valid')
        if not json.loads((original / 'agent/isolation-audit.json').read_text())['passed']:
            raise RuntimeError('Original isolation failed')
        if 'Trace/breakpoint trap' not in (original / 'verifier/test-stdout.txt').read_text():
            raise RuntimeError('Missing original database interruption evidence')
        archive = ROOT / 'infrastructure/attempts' / (job + '--grader-mongo-20261030')
        shutil.copytree(original.parent, archive)
        parent = ROOT / 'recoveries' / job
        parent.mkdir(parents=True, exist_ok=False)
        write_json(parent / 'started.json', {
            'started_at': datetime.now(timezone.utc).isoformat(), 'pid': os.getpid(),
            'original_trial': original.name, 'original_archive': str(archive.relative_to(ROOT)),
            'additional_model_executions': 0, 'repair': 'nofile soft1024 to65536; hard524288 unchanged',
        })
        config = TrialConfig.model_validate_json((original / 'config.json').read_text())
        config.trials_dir = parent
        config.trial_name = original.name + '-grader-recovery'
        config.environment.import_path = 'recover_eicrud_verifiers:MongoGraderEnvironment'
        trial = await Trial.create(config)
        write_json(trial.trial_dir / 'config.json', config.model_dump(mode='json'))
        shutil.copytree(original / 'artifacts', trial.trial_dir / 'artifacts', dirs_exist_ok=True)
        started = datetime.now(timezone.utc)
        print(json.dumps({'event': 'grader_start', 'job': job, 'time': started.isoformat()}), flush=True)
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
        stdout = (trial.trial_dir / 'verifier/test-stdout.txt').read_text()
        database = json.loads((trial.trial_dir / 'database-after.json').read_text())
        mongolog = (trial.trial_dir / 'verifier/mongod-recovery.log').read_text()
        if 'Trace/breakpoint trap' in stdout or 'Too many open files' in mongolog or not re.search(r'MONGO_PID=\d+', database['stdout'] or ''):
            raise RuntimeError('Database recovery remains interrupted; preserve and diagnose without automatic retry')
        if result.rewards != grade or grade.get('reward') not in [0, 1] or stdout.count('===== grade =====') != 1:
            raise RuntimeError('Official grading output mismatch')
        if grade['f2p_total'] != 14 or grade['p2p_total'] != 168:
            raise RuntimeError('Unexpected official test population')
        receipt = {
            'passed': True, 'classification': 'verifier_mongodb_nofile_crash',
            'trial': original.name, 'job': job, 'model_executions': 1, 'verifier_executions': 2,
            'additional_model_executions': 0, 'original_result_preserved': True,
            'original_patch_preserved': True, 'original_verifier_preserved': True,
            'original_archive': str(archive.relative_to(ROOT)),
            'recovery_directory': str(trial.trial_dir.relative_to(ROOT)),
            'recovery_seconds': (finished - started).total_seconds(), 'recovered_at': finished.isoformat(),
            'reward': grade['reward'], 'original_reward': raw['verifier_result']['rewards'],
            'repair': 'Only verifier nofile soft limit1024 to65536; existing hard524288, CPU/RAM, tests and model.patch unchanged',
        }
        write_json(original / 'verifier-recovery.json', receipt)
        reviewed_verifier_recovery(original)
        status.update(status='completed', receipt=str((original / 'verifier-recovery.json').relative_to(ROOT)))
        pending['updated_at'] = finished.isoformat()
        write_json(pending_path, pending)
        print(json.dumps({'event': 'grader_complete', **receipt}), flush=True)
    write_json(ROOT / 'infrastructure/eicrud-recovery-complete.json', {
        'finished_at': datetime.now(timezone.utc).isoformat(), 'additional_model_executions': 0,
        'jobs': pending['jobs'], 'dedicated_containers_remaining': subprocess.check_output(['docker', 'ps', '-q'], text=True).split(),
    })


if __name__ == '__main__':
    asyncio.run(main())
