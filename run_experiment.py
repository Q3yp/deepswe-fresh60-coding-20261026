from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import subprocess

from pier.job import Job
from pier.models.job.config import JobConfig


ROOT = Path(__file__).resolve().parent
PLAN = json.loads((ROOT / 'experiment-plan.json').read_text())
SOCKET = 'unix:///Users/huizai/.colima/codex-deepswe/docker.sock'


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n')


def record(event, **fields):
    data = {'time': datetime.now(timezone.utc).isoformat(), 'event': event, **fields}
    with (ROOT / 'events.jsonl').open('a') as handle:
        handle.write(json.dumps(data) + '\n')
    print(json.dumps(data), flush=True)


def rewards(results):
    return [(r.get('verifier_result') or {}).get('rewards', {}).get('reward') for r in results]


async def run_job(name, task, agent):
    directory = ROOT / 'jobs' / name
    if (directory / 'result.json').exists():
        previous = json.loads((directory / 'result.json').read_text())
        if not previous.get('finished_at'):
            raise RuntimeError(f'Incomplete job needs inspection: {name}')
        record('job_reused', job=name)
        return [json.loads(p.read_text()) for p in sorted(directory.glob('*/result.json'))]
    if directory.exists():
        raise RuntimeError(f'Unfinished job directory needs inspection: {name}')
    if shutil.disk_usage(ROOT).free < 15 * 1024**3:
        raise RuntimeError('Host free space is below the reserved 15 GiB')
    configuration = JobConfig.model_validate({
        'job_name': name, 'jobs_dir': str(ROOT / 'jobs'),
        'n_attempts': 1, 'n_concurrent_trials': 1, 'quiet': True,
        'retry': {'max_retries': 0},
        'environment': {'type': 'docker', 'delete': False},
        'agents': [agent], 'tasks': [{'path': str(ROOT / 'tasks' / task)}],
    })
    record('job_start', job=name, task=task)
    job = await Job.create(configuration)
    await job.run()
    results = [json.loads(p.read_text()) for p in sorted(directory.glob('*/result.json'))]
    record('job_finish', job=name, rewards=rewards(results), exceptions=[
        (r.get('exception_info') or {}).get('exception_type') for r in results
    ])
    return results


def prune_task_cache():
    if os.environ.get('DOCKER_HOST') != SOCKET:
        raise RuntimeError('Refusing cache cleanup outside the dedicated Docker socket')
    active = subprocess.check_output(['docker', 'ps', '-q'], text=True).strip()
    if active:
        raise RuntimeError('Containers remain active; retain them for inspection')
    for command in [['docker', 'image', 'prune', '-af'], ['docker', 'builder', 'prune', '-af']]:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        record('cache_cleanup', command=command, output=result.stdout[-1200:])

