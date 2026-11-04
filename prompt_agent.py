import json
from pathlib import Path, PurePosixPath

from pier.agents.installed.codex import Codex
from pier.models.agent.network import NetworkAllowlist


class PromptCodex(Codex):
    _REMOTE_CODEX_HOME = PurePosixPath('/installed-agent/codex-home')

    def __init__(self, *args, prompt_path, conveying_path, **kwargs):
        self.prompt_path = Path(prompt_path)
        self.conveying_path = Path(conveying_path)
        super().__init__(*args, **kwargs)

    def network_allowlist(self):
        return NetworkAllowlist(domains=['api.openai.com', 'chatgpt.com', 'auth.openai.com'])

    async def setup(self, environment):
        await super().setup(environment)
        await environment.upload_file(self.prompt_path, '/installed-agent/base-instructions.md')
        await super().exec_as_agent(
            environment, command=f'mkdir -p {self._REMOTE_CODEX_HOME}/skills/conveying'
        )
        await environment.upload_file(
            self.conveying_path, f'{self._REMOTE_CODEX_HOME}/skills/conveying/SKILL.md'
        )
        await environment.upload_file(
            Path(__file__).with_name('audit_isolation.py'), '/installed-agent/audit_isolation.py'
        )

    async def exec_as_agent(self, environment, command, env=None, cwd=None, timeout_sec=None):
        if 'codex exec ' in command:
            audit = await super().exec_as_agent(
                environment,
                command='if [ -s ~/.nvm/nvm.sh ]; then . ~/.nvm/nvm.sh; fi; python3 /installed-agent/audit_isolation.py',
                env=env, cwd=cwd, timeout_sec=100,
            )
            report = json.loads(audit.stdout)
            (self.logs_dir / 'isolation-audit.json').write_text(json.dumps(report, indent=2))
            if not report['passed']:
                raise RuntimeError('Codex isolation audit failed before model execution')
            command = 'set -o pipefail; ' + command
        return await super().exec_as_agent(
            environment, command=command, env=env, cwd=cwd, timeout_sec=timeout_sec
        )
