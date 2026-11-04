import json
from pathlib import Path


def reviewed_verifier_recovery(trial):
    receipt_path = trial / 'verifier-recovery.json'
    if not receipt_path.exists():
        return None
    receipt = json.loads(receipt_path.read_text())
    root = Path(__file__).resolve().parent
    recovery = root / receipt['recovery_directory']
    archive = root / receipt['original_archive'] / trial.name
    raw = json.loads((trial / 'result.json').read_text())
    result = json.loads((recovery / 'verification-result.json').read_text())
    grade = json.loads((recovery / 'verifier/reward.json').read_text())
    if receipt['classification'] == 'verifier_mongodb_nofile_crash':
        original_verifier = trial / 'verifier'
        archived_verifier = archive / 'verifier'
        import re
        database = json.loads((recovery / 'database-after.json').read_text())
        limits = json.loads((recovery / 'limits-before.json').read_text())
        valid = (
            receipt['trial'] == trial.name and receipt['job'] == trial.parent.name
            and trial.parent.name.startswith('eicrud-keyset-pagination-cursor--')
            and receipt['passed'] and receipt['additional_model_executions'] == 0
            and receipt['model_executions'] == 1 and receipt['verifier_executions'] == 2
            and raw['exception_info'] is None and raw['verifier_result']['rewards']['reward'] == 0
            and 'Trace/breakpoint trap' in (original_verifier / 'test-stdout.txt').read_text()
            and (archive / 'result.json').read_bytes() == (trial / 'result.json').read_bytes()
            and (archive / 'artifacts/model.patch').read_bytes() == (trial / 'artifacts/model.patch').read_bytes()
            and (recovery / 'artifacts/model.patch').read_bytes() == (trial / 'artifacts/model.patch').read_bytes()
            and all((original_verifier / p.relative_to(archived_verifier)).read_bytes() == p.read_bytes() for p in archived_verifier.rglob('*') if p.is_file())
            and result['verifier_result']['rewards'] == grade
            and grade['reward'] == receipt['reward'] and grade['reward'] in [0, 1]
            and grade['f2p_total'] == 14 and grade['p2p_total'] == 168
            and (recovery / 'verifier/test-stdout.txt').read_text().count('===== grade =====') == 1
            and 'Trace/breakpoint trap' not in (recovery / 'verifier/test-stdout.txt').read_text()
            and 'Too many open files' not in (recovery / 'verifier/mongod-recovery.log').read_text()
            and re.search(r'MONGO_PID=\d+', database['stdout'] or '')
            and re.search(r'Max open files\s+65536\s+524288', limits['stdout'] or '')
        )
        if not valid:
            raise RuntimeError(f'MongoDB verifier recovery does not match retained evidence: {trial}')
        return receipt
    valid = (
        ((receipt['classification'] == 'verifier_registry_tls_before_execution' and 'TLS handshake timeout' in raw['exception_info']['exception_message'])
         or (receipt['classification'] == 'verifier_registry_io_before_execution' and 'load metadata for public.ecr.aws' in raw['exception_info']['exception_message'] and 'dial tcp 198.18.0.59:443: i/o timeout' in raw['exception_info']['exception_message']))
        and receipt['trial'] == trial.name and receipt['job'] == trial.parent.name
        and receipt['passed'] and receipt['additional_model_executions'] == 0
        and receipt['model_executions'] == receipt['verifier_executions'] == 1
        and (raw.get('exception_info') or {}).get('exception_type') == 'RuntimeError'
        and raw.get('verifier_result') is None
        and (archive / 'result.json').read_bytes() == (trial / 'result.json').read_bytes()
        and (archive / 'artifacts/model.patch').read_bytes() == (trial / 'artifacts/model.patch').read_bytes()
        and (recovery / 'artifacts/model.patch').read_bytes() == (trial / 'artifacts/model.patch').read_bytes()
        and result['verifier_result']['rewards'] == grade
        and grade == json.loads((trial / 'verifier/reward.json').read_text())
        and grade == json.loads((recovery / 'verifier/reward.json').read_text())
        and (trial / 'verifier/test-stdout.txt').read_text().count('===== grade =====') == 1
        and grade['reward'] == receipt['reward'] and grade['reward'] in [0, 1]
    )
    if not valid:
        raise RuntimeError(f'Verifier recovery does not match retained evidence: {trial}')
    return receipt
