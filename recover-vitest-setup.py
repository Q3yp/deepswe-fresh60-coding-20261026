import fcntl
import json
import os
from pathlib import Path
import subprocess
from datetime import datetime, timezone

root = Path(__file__).resolve().parent
shared = root.parents[1]
os.environ.update(
    PATH='/opt/homebrew/bin:/usr/local/bin:/Users/huizai/.local/bin:' + os.environ['PATH'],
    DOCKER_HOST='unix:///Users/huizai/.colima/codex-deepswe/docker.sock',
    DOCKER_CONFIG=str(shared / 'docker-config'),
    DOCKER_DEFAULT_PLATFORM='linux/amd64',
)
os.environ.pop('DOCKER_CONTEXT', None)
lock = (shared / 'runner.lock').open('a')
fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
assert not subprocess.check_output(['docker', 'ps', '-q'], text=True).strip()
builds = subprocess.check_output(['docker', 'buildx', 'history', 'ls', '--format', 'json'], text=True)
assert not any(json.loads(line)['status'] == 'Running' for line in builds.splitlines())
assert (shared / 'jobs/ink-grid-box-layout--override--r1/operator-stop.json').exists()
job = root / 'jobs/vitest-duration-sharding--bundled--r1'
native = job / 'vitest-duration-sharding__tLyyJsi/result.json'
result = json.loads(native.read_text())
assert result['finished_at'] and result['exception_info']['exception_type'] == 'EnvironmentStartTimeoutError'
assert all(result.get(key) is None for key in ['agent_setup', 'agent_execution', 'agent_result', 'verifier', 'verifier_result'])
assert not list(job.glob('*/agent/sessions/**/*.jsonl'))
assert not list(job.glob('*/verifier/reward.json'))
manifest = json.loads((root / 'infrastructure/vitest-bundled-r1-setup-timeout.json').read_text())
archive = root / manifest['archive']
assert not archive.exists()
plan = json.loads((root / 'experiment-plan.json').read_text())
for item in plan['schedule'][:24]:
    name = f"{item['task']}--{item['condition']}--r{item['repeat']}"
    results = list((root / 'jobs' / name).glob('*/result.json'))
    assert len(results) == 1
    assert json.loads(results[0].read_text())['verifier_result']['rewards']['reward'] in [0, 1]

status_path = root / 'infrastructure/vitest-setup-recovery-status.json'
def record(stage, **fields):
    data = {'updated_at': datetime.now(timezone.utc).isoformat(), 'pid': os.getpid(), 'stage': stage, **fields}
    status_path.write_text(json.dumps(data, indent=2) + '\n')
    print(json.dumps(data), flush=True)

record('pulling_original_image', image=manifest['image'], retained_scores=24)
pull = subprocess.run(['docker', 'pull', '--platform', 'linux/amd64', manifest['image']], timeout=1800)
if pull.returncode:
    record('image_pull_failed', returncode=pull.returncode)
    raise SystemExit(pull.returncode)
tag = next(task['image'] for task in plan['tasks'] if task['name'] == 'vitest-duration-sharding')
subprocess.run(['docker', 'tag', manifest['image'], tag], check=True)
archive.parent.mkdir(parents=True, exist_ok=True)
job.rename(archive)
record('resuming_queue', retained_scores=24, archived_failed_setup=str(archive))
fcntl.flock(lock, fcntl.LOCK_UN)
lock.close()
os.chdir(root)
os.execv('/bin/bash', ['/bin/bash', str(root / 'launch.sh')])
