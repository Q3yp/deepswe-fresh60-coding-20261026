import asyncio
import json
import os
from datetime import datetime, timezone
from pathlib import Path


async def main():
    home = Path(os.environ["CODEX_HOME"]).resolve()
    expected_skill = home / "skills" / "conveying" / "SKILL.md"
    process = await asyncio.create_subprocess_exec(
        "codex", "app-server", "--strict-config",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    async def rpc(request_id, method, params):
        process.stdin.write((json.dumps({
            "id": request_id, "method": method, "params": params,
        }) + "\n").encode())
        await process.stdin.drain()
        async with asyncio.timeout(30):
            while line := await process.stdout.readline():
                message = json.loads(line)
                if message.get("id") == request_id:
                    if "error" in message:
                        raise RuntimeError(f"{method}: {message['error']}")
                    return message["result"]
        raise RuntimeError(f"App server exited during {method}")

    try:
        initialized = await rpc(1, "initialize", {
            "clientInfo": {"name": "deepswe-isolation-audit", "version": "1"},
            "capabilities": {"experimentalApi": True},
        })
        process.stdin.write(b'{"method":"initialized"}\n')
        await process.stdin.drain()
        inventory = await rpc(2, "skills/list", {
            "cwds": [str(Path.cwd())], "forceReload": True,
        })
        disabled_skills = []
        for entry in inventory["data"]:
            for skill in entry["skills"]:
                if skill["enabled"] and Path(skill["path"]).resolve() != expected_skill:
                    result = await rpc(100 + len(disabled_skills), "skills/config/write", {
                        "path": skill["path"], "enabled": False,
                    })
                    if result["effectiveEnabled"]:
                        raise RuntimeError(f"Skill remains enabled: {skill['path']}")
                    disabled_skills.append(skill["path"])
        if disabled_skills:
            inventory = await rpc(4, "skills/list", {
                "cwds": [str(Path.cwd())], "forceReload": True,
            })
        effective = (await rpc(3, "config/read", {
            "includeLayers": False, "cwd": str(Path.cwd()),
        }))["config"]
        skills = [skill for entry in inventory["data"] for skill in entry["skills"]]
        errors = [error for entry in inventory["data"] for error in entry["errors"]]
        enabled = [skill for skill in skills if skill["enabled"]]
        memory_files = [str(path.relative_to(home)) for path in
                        (home / "memories").rglob("*") if path.is_file()]
        checks = {
            "only_conveying_enabled": len(enabled) == 1
            and enabled[0]["name"] == "conveying"
            and Path(enabled[0]["path"]).resolve() == expected_skill,
            "skill_catalog_has_no_errors": not errors,
            "memory_use_disabled": effective["memories"]["use_memories"] is False,
            "memory_generation_disabled": effective["memories"]["generate_memories"] is False,
            "no_memory_files": not memory_files,
            "bundled_skills_disabled": effective["skills"]["bundled"]["enabled"] is False,
            **{f"{feature}_disabled": effective["features"][feature] is False
               for feature in ("memories", "plugins", "apps", "multi_agent")},
        }
        report = {
            "time": datetime.now(timezone.utc).isoformat(),
            "runtime": initialized,
            "cwd": str(Path.cwd()),
            "checks": checks,
            "passed": all(checks.values()),
            "skills": skills,
            "disabled_skills": disabled_skills,
            "skill_errors": errors,
            "memory_files": memory_files,
            "effective_config": {key: effective[key] for key in (
                "memories", "features", "skills", "model_instructions_file",
                "model_reasoning_effort", "model_verbosity",
            )},
        }
        print(json.dumps(report, indent=2), flush=True)
        if not report["passed"]:
            raise RuntimeError("Runtime isolation audit failed")
    finally:
        if process.returncode is None:
            process.terminate()
        await asyncio.wait_for(process.wait(), timeout=5)


if __name__ == "__main__":
    asyncio.run(main())
