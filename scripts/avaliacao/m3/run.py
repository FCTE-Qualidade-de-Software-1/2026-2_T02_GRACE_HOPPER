#!/usr/bin/env python3
"""Execute a frozen M3 manifest and reconcile results against planned IDs."""
import argparse
import difflib
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent


def verify_manifest():
    """Reject a manifest that differs from the recorded reference digest."""
    expected, name = (HERE / 'manifest.sha256').read_text().split()
    if name != 'manifest.json':
        raise RuntimeError('Unexpected manifest filename in manifest.sha256')
    actual = hashlib.sha256((HERE / name).read_bytes()).hexdigest()
    if actual != expected:
        raise RuntimeError('Manifest differs from manifest.sha256; no suite executed')
    return actual


def consolidate(manifest, xml_path, exit_code):
    ids = [c['id'] for c in manifest['cases']]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate IDs in manifest')
    found = {}
    anomalies = []
    if xml_path.exists():
        try:
            for case in ET.parse(xml_path).iter('testcase'):
                match = re.search(r'\bM3 ([A-Z][0-9]{2})\b', case.get('name', ''))
                if not match:
                    anomalies.append('Unknown test: ' + case.get('name', ''))
                    continue
                cid = match[1]
                status = 'passed'
                for tag in ('failure', 'error', 'skipped'):
                    if case.find(tag) is not None:
                        status = tag
                found.setdefault(cid, []).append(status)
        except ET.ParseError as exc:
            anomalies.append('Invalid JUnit: ' + str(exc))
    rows = []
    for cid in ids:
        states = found.get(cid, [])
        rows.append({'id': cid, 'status': states[0] if len(states) == 1 else ('duplicate' if states else 'missing')})
    anomalies.extend('Unknown ID: ' + cid for cid in found if cid not in ids)
    good = sum(r['status'] == 'passed' for r in rows)
    n = len(ids)
    approved = n > 0 and good == n and not anomalies and exit_code == 0
    return {'planned': n, 'conforming': good, 'nonconforming': n-good,
            'fraction': f'{good}/{n}', 'percent_exact': str(Fraction(good * 100, n)) if n else None,
            'percent': good * 100 / n if n else None, 'gate': 'APROVADO' if approved else 'BLOQUEADO',
            'cases': rows, 'anomalies': anomalies, 'exit_code': exit_code}


def consolidate_legacy(xml_path, exit_code):
    """Report reactivated upstream tests separately from the frozen M3 universe."""
    report = {'exit_code': exit_code, 'included_in_dcnm': False, 'cases': []}
    if not xml_path.exists():
        report['error'] = 'Legacy JUnit not produced; outcomes not verified'
        return report
    for case in ET.parse(xml_path).iter('testcase'):
        row = {'name': case.get('name'), 'class': case.get('class'), 'status': 'passed'}
        for tag in ('failure', 'error', 'skipped'):
            detail = case.find(tag)
            if detail is not None:
                row.update(status=tag, exception=detail.get('type'), detail=(detail.text or '').strip())
        if (row.get('exception') or '').split('\\')[-1] in (
                'StudentNotEnrolledInSchoolClass', 'EvaluationRuleNotDefinedInLevel'):
            row['classification'] = 'fixture_prerequisite_missing'
        elif row['status'] != 'passed':
            row['classification'] = 'requires_investigation'
        report['cases'].append(row)
    report['total'] = len(report['cases'])
    report['passed'] = sum(c['status'] == 'passed' for c in report['cases'])
    report['fixture_blocked'] = sum(c.get('classification') == 'fixture_prerequisite_missing' for c in report['cases'])
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--product', type=Path, required=True, help='Isolated clean checkout at the required commit')
    parser.add_argument('--output', type=Path, required=True, help='New evidence directory')
    parser.add_argument('--php-command', default='php', help='PHP invocation, e.g. docker compose exec -T php php')
    parser.add_argument('--diagnostic', action='store_true', help='Allow uncommitted instruments; cannot grant official acceptance')
    args = parser.parse_args()
    product = args.product.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    manifest = json.loads((HERE / 'manifest.json').read_text())
    metadata = {'started_utc': datetime.now(timezone.utc).isoformat(), 'product_commit_required': manifest['product_commit']}
    failure = None
    code = 2
    injected = []
    runtime_env = dict(os.environ, M3_PRODUCT_DIR=str(product))
    try:
        metadata['manifest_reference_sha256'] = verify_manifest()
        commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=product, text=True).strip()
        metadata['product_commit_actual'] = commit
        if commit != manifest['product_commit']:
            raise RuntimeError('Product commit differs from manifest; no suite executed')
        if subprocess.check_output(['git', 'status', '--porcelain'], cwd=product, text=True).strip():
            raise RuntimeError('Product checkout must be clean before injection')
        metadata['instrument_commit'] = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=HERE, text=True).strip()
        metadata['instrument_dirty'] = bool(subprocess.check_output(
            ['git', 'status', '--porcelain', '--', str(HERE)], cwd=HERE, text=True).strip())
        metadata['execution_mode'] = 'diagnostic' if args.diagnostic else 'official'
        if metadata['instrument_dirty'] and not args.diagnostic:
            raise RuntimeError('Version the instrument and manifest before official execution')
        for name in ('manifest.json', 'M3OracleTest.php', 'run.py'):
            metadata[name + '_sha256'] = hashlib.sha256((HERE / name).read_bytes()).hexdigest()
        snapshot = output / 'instrument'
        snapshot.mkdir()
        for name in ('manifest.json', 'manifest.sha256', 'M3OracleTest.php', 'run.py', 'run_local.py', 'compose.yml', 'php.sh'):
            shutil.copyfile(HERE / name, snapshot / name)
        metadata['composer_lock_sha256'] = hashlib.sha256((product / 'composer.lock').read_bytes()).hexdigest()
        php = shlex.split(args.php_command)
        version = subprocess.run(php + ['-v'], cwd=product, env=runtime_env, capture_output=True, text=True)
        metadata['php_version'] = version.stdout + version.stderr
        if version.returncode or not re.search(r'PHP 8\.5\.', version.stdout):
            raise RuntimeError('PHP 8.5 required')
        destination = product / 'tests/Unit/Modules/Service'
        targets = [destination / 'M3OracleTest.php', destination / 'm3-manifest.json']
        if any(t.exists() for t in targets):
            raise RuntimeError('Injected filenames already exist; use a fresh isolated checkout')
        shutil.copyfile(HERE / 'M3OracleTest.php', targets[0])
        injected.append(targets[0])
        shutil.copyfile(HERE / 'manifest.json', targets[1])
        injected.append(targets[1])
        # Verify the container is reading the same checkout and instrument as the host.
        checked_paths = ['composer.lock', 'ieducar/modules/Avaliacao/Service/Boletim.php',
                         'tests/Unit/Modules/Service/M3OracleTest.php',
                         'tests/Unit/Modules/Service/m3-manifest.json']
        fingerprint_code = '$r=[]; foreach (json_decode($argv[1],true) as $p) {$r[$p]=hash_file("sha256",$p);} echo json_encode($r);'
        runtime_hashes = json.loads(subprocess.check_output(
            php + ['-r', fingerprint_code, json.dumps(checked_paths)], cwd=product,
            env=runtime_env, text=True))
        host_hashes = {name: hashlib.sha256((product / name).read_bytes()).hexdigest() for name in checked_paths}
        metadata['runtime_file_sha256'] = runtime_hashes
        if runtime_hashes != host_hashes:
            raise RuntimeError('Runtime checkout differs from host checkout; no suite executed')
        # A path inside the product also works when PHP runs in its container.
        junit = product / 'm3-junit.xml'
        if junit.exists():
            raise RuntimeError('Existing JUnit output would risk stale evidence')
        injected.append(junit)
        command = php + ['vendor/bin/pest', 'tests/Unit/Modules/Service/M3OracleTest.php', '--colors=never', '--log-junit=m3-junit.xml']
        metadata['command'] = command
        with (output / 'execution.txt').open('w') as log:
            with subprocess.Popen(command, cwd=product, env=runtime_env, stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT, text=True) as process:
                for line in process.stdout:
                    log.write(line)
                    log.flush()
                    print(line, end='', flush=True)
                code = process.wait()
        if junit.exists():
            shutil.copyfile(junit, output / 'junit.xml')
        # Complementary legacy scenarios: activate only in this disposable checkout.
        legacy = destination / 'NotaSituacaoCommon.php'
        original = legacy.read_text()
        metadata['legacy_original_sha256'] = hashlib.sha256(legacy.read_bytes()).hexdigest()
        metadata['legacy_skips_removed'] = original.count('$this->markTestSkipped();')
        legacy_junit = product / 'm3-legacy-junit.xml'
        if legacy_junit.exists():
            raise RuntimeError('Existing legacy JUnit output would risk stale evidence')
        injected.append(legacy_junit)
        try:
            reactivated = original.replace('$this->markTestSkipped();', '')
            legacy.write_text(reactivated)
            (output / 'legacy-reactivation.patch').write_text(''.join(difflib.unified_diff(
                original.splitlines(keepends=True), reactivated.splitlines(keepends=True),
                fromfile='a/tests/Unit/Modules/Service/NotaSituacaoCommon.php',
                tofile='b/tests/Unit/Modules/Service/NotaSituacaoCommon.php')))
            legacy_command = php + ['vendor/bin/pest',
                'tests/Unit/Modules/Service/NotaNumericaSituacaoTest.php',
                'tests/Unit/Modules/Service/NotaConceitualSituacaoTest.php', '--colors=never',
                '--log-junit=m3-legacy-junit.xml']
            metadata['legacy_command'] = legacy_command
            with (output / 'legacy.txt').open('w') as log:
                metadata['legacy_exit_code'] = subprocess.run(legacy_command, cwd=product, env=runtime_env,
                    stdout=log, stderr=subprocess.STDOUT).returncode
            if legacy_junit.exists():
                shutil.copyfile(legacy_junit, output / 'legacy-junit.xml')
            (output / 'legacy-summary.json').write_text(json.dumps(consolidate_legacy(
                output / 'legacy-junit.xml', metadata['legacy_exit_code']), indent=2) + '\n')
        finally:
            legacy.write_text(original)
    except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
        failure = str(exc)
        with (output / 'execution.txt').open('a') as log:
            log.write('\nExecutor error: ' + failure + '\n')
    finally:
        for path in injected:
            path.unlink(missing_ok=True)
    metadata['preflight_error'] = failure
    metadata['finished_utc'] = datetime.now(timezone.utc).isoformat()
    (output / 'environment.json').write_text(json.dumps(metadata, indent=2) + '\n')
    shutil.copyfile(HERE / 'manifest.json', output / 'manifest.json')
    shutil.copyfile(HERE / 'manifest.sha256', output / 'manifest.sha256')
    summary = consolidate(manifest, output / 'junit.xml', code)
    summary['execution_attempted'] = 'command' in metadata
    summary['preflight_error'] = failure
    raw = (output / 'execution.txt').read_text()
    values = {}
    for match in re.finditer(r'M3_RESULT (\{[^\n]*?\})', raw):
        try:
            value = json.loads(match[1])
            values[value['id']] = value
        except (ValueError, KeyError):
            pass
    expected = {c['id']: c['expected'] for c in manifest['cases']}
    for row in summary['cases']:
        row['expected'] = expected[row['id']]
        row['actual'] = values.get(row['id'], {}).get('actual')
    for row in summary['cases']:
        if row['status'] == 'passed' and row['actual'] is None:
            row['status'] = 'missing_evidence'
    summary['conforming'] = sum(r['status'] == 'passed' for r in summary['cases'])
    summary['nonconforming'] = summary['planned'] - summary['conforming']
    good, total = summary['conforming'], summary['planned']
    summary['fraction'] = f'{good}/{total}'
    summary['percent_exact'] = str(Fraction(good * 100, total)) if total else None
    summary['percent'] = good * 100 / total if total else None
    if good != total or failure:
        summary['gate'] = 'BLOQUEADO'
    summary['technical_gate'] = summary['gate']
    summary['execution_mode'] = 'diagnostic' if args.diagnostic else 'official'
    summary['official_acceptance'] = summary['gate'] == 'APROVADO' and not args.diagnostic
    if args.diagnostic:
        summary['gate'] = 'BLOQUEADO'
    (output / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    (output / 'results.csv').write_text('id,status,expected,actual\n' + ''.join(f"{r['id']},{r['status']},{r['expected']},{r['actual']}\n" for r in summary['cases']))
    print(json.dumps({k: summary[k] for k in (
        'gate', 'technical_gate', 'execution_mode', 'official_acceptance', 'fraction', 'preflight_error'
    )}, ensure_ascii=False))
    return 0 if summary['technical_gate'] == 'APROVADO' else 1


if __name__ == '__main__':
    raise SystemExit(main())
