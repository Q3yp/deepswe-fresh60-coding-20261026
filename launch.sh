#!/bin/bash
set -euo pipefail
task_root=$(cd -- "$(dirname -- "$0")" && pwd)
export PATH="/opt/homebrew/bin:/usr/local/bin:/Users/huizai/.local/bin:$PATH"
export DOCKER_CONFIG="/Users/huizai/.t3/benchmarks/codex-base-deepswe-20261022/docker-config"
export DOCKER_HOST="unix:///Users/huizai/.colima/codex-deepswe/docker.sock"
export DOCKER_DEFAULT_PLATFORM="linux/amd64"
unset DOCKER_CONTEXT OPENAI_API_KEY OPENAI_BASE_URL
cd "$task_root"
exec caffeinate -i /Users/huizai/.t3/benchmarks/codex-base-deepswe-20261022/.venv/bin/python run_batch.py
