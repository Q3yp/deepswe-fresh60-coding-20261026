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
assert subprocess.run(['pgrep', '-f', 'run_batch.py'], capture_output=True).returncode == 1
assert not subprocess.check_output(['docker', 'ps', '-aq'], text=True).strip()
builds = subprocess.check_output(['docker', 'buildx', 'history', 'ls', '--format', 'json'], text=True)
assert not any(json.loads(line)['status'] == 'Running' for line in builds.splitlines())
assert (shared / 'jobs/ink-grid-box-layout--override--r1/operator-stop.json').exists()

job = root / 'jobs/ytt-jsonpath-query-api--bundled--r1'
native = job / 'ytt-jsonpath-query-api__TjBvQZh/result.json'
result = json.loads(native.read_text())
assert result['finished_at'] and result['exception_info']['exception_type'] == 'EnvironmentStartTimeoutError'
assert all(result.get(key) is None for key in ['agent_setup', 'agent_execution', 'agent_result', 'verifier', 'verifier_result'])
assert not list(job.glob('*/agent/sessions/**/*.jsonl'))
assert not list(job.glob('*/verifier/reward.json'))
archive = root / 'infrastructure/attempts/ytt-jsonpath-query-api--bundled--r1--setup-timeout-20261028T043509Z'
assert not archive.exists()
archive.parent.mkdir(parents=True, exist_ok=True)
job.rename(archive)
provenance = {
    'archived_at': datetime.now(timezone.utc).isoformat(),
    'original_job': str(job), 'archive': str(archive),
    'reason': 'Base image layer download stalled at 17.83/22.79 MB; environment setup timed out before agent or grader.',
    'model_started': False, 'grader_started': False, 'reward': None,
    'original_records_preserved': True,
}
(archive / 'archive-provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
status_path = root / 'infrastructure/ytt-setup-recovery-status-20261028.json'


def record(stage, **fields):
    data = {'updated_at': datetime.now(timezone.utc).isoformat(), 'pid': os.getpid(), 'stage': stage, **fields}
    status_path.write_text(json.dumps(data, indent=2) + '\n')
    print(json.dumps(data), flush=True)


image = 'public.ecr.aws/d3j8x8q7/swe-bench-202605@sha256:34d04ef8efcbbcb74b634e35141bd2defde29cd01073cc3ba07b2b70aa911bdf'
record('pulling_original_image', image=image, retained_scores=101, archive=str(archive))
pull = subprocess.run(['docker', 'pull', '--platform', 'linux/amd64', image], timeout=1800)
if pull.returncode:
    record('image_pull_failed', returncode=pull.returncode)
    raise SystemExit(pull.returncode)
plan = json.loads((root / 'experiment-plan.json').read_text())
tag = next(task['image'] for task in plan['tasks'] if task['name'] == 'ytt-jsonpath-query-api')
subprocess.run(['docker', 'tag', image, tag], check=True)
record('resuming_queue', retained_scores=101, archived_failed_setup=str(archive))
fcntl.flock(lock, fcntl.LOCK_UN)
lock.close()
os.chdir(root)
os.execv('/bin/bash', ['/bin/bash', str(root / 'launch.sh')])
