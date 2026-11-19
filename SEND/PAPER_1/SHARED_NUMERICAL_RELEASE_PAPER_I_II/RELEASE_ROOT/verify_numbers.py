from __future__ import annotations

import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def close(a, b, tol=1e-10):
    return math.isclose(float(a), float(b), rel_tol=0.0, abs_tol=tol)


def sha256(path):
    import hashlib
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def main():
    checks = []
    core = {}
    with (ROOT / '00_MANUSCRIPT/PAPER_IV_CORE_NUMBERS.tsv').open(encoding='utf-8') as f:
        for row in csv.DictReader(f, delimiter='\t'):
            core[row['KEY']] = row['VALUE']
    expected_core = {
        'DEV99_EVENTS': '99', 'PATH_FOUND': '98', 'NO_PATH': '1',
        'FROZEN_NODES': '1083', 'FROZEN_TRANSITIONS': '985',
        'RARITY_COMPLEXITY_SPEARMAN': '0.6619802493',
        'RARITY_COMPLEXITY_P': '0.0001', 'PHYSICAL_CLOCK_GAMMA': '0.3162354634',
        'R38_PRIMARY_P': '0.0006', 'R38_FIXED_SCORE_P': '0.0001',
        'R41_PRIMARY_P': '0.004', 'R41_FIXED_P1_P': '0.002',
    }
    for key, value in expected_core.items():
        checks.append((key, core.get(key) == value))

    law = json.loads((ROOT / '01_NUMERICAL_RESULTS/PAPER_IV/04_FROZEN_RULES/R40_CANONICAL_LAW.json').read_text(encoding='utf-8'))
    checks.append(('GAMMA_FROZEN', close(law['PHYSICAL_COEFFICIENT']['gamma_ALL'], 0.3162354634393393)))

    summary = json.loads((ROOT / '01_NUMERICAL_RESULTS/PAPER_IV/FINAL101/R40_W4_POWER_AUDIT_SUMMARY.json').read_text(encoding='utf-8'))
    checks += [
        ('W4_POWER_N', summary.get('N_RESAMPLE') == 9999),
        ('W4_POWER_P', close(summary.get('P_W4_DIRECTION_FAIL_AT_N4'), 0.8734873487348734)),
        ('W4_VERDICT', summary.get('W4_VERDICT') == 'W4_LIKELIHOOD_REPLICATED_DIRECTION_UNDERPOWERED'),
    ]

    rows = list(csv.DictReader((ROOT / '01_NUMERICAL_RESULTS/PAPER_IV/FINAL101/R40_FINAL_101_MAP_CHARACTERIZATION.csv').open(encoding='utf-8')))
    checks.append(('FINAL101_ROWS', len(rows) == 12))
    expected = {
        ('DEV96', 'W1_START_TO_PEAK'): 2.5983730031069854,
        ('DEV96', 'W2_PEAK_TO_END'): 4.598773450207091,
        ('DEV96', 'W3_START_TO_MT'): 2.4619078574406785,
        ('DEV96', 'W4_MT_TO_END'): 4.735238595873284,
        ('HOLDOUT5', 'W1_START_TO_PEAK'): 1.1043334444486135,
        ('HOLDOUT5', 'W2_PEAK_TO_END'): 0.2230157036802467,
        ('HOLDOUT5', 'W3_START_TO_MT'): 1.0415943943363075,
        ('HOLDOUT5', 'W4_MT_TO_END'): 0.134886435093442,
    }
    for row in rows:
        key = (row['BLOCK'], row['MAP_NAME'])
        if key in expected:
            checks.append((f'DELTA_LOGLIK_{key[0]}_{key[1]}', close(row['DELTA_LOGLIK'], expected[key])))

    origin_path = ROOT / '03_PROVENANCE/ORIGIN_SHA256.tsv'
    origin_rows = list(csv.DictReader(origin_path.open(encoding='utf-8'), delimiter='\t'))
    checks.append(('PAPER_I_II_ORIGIN_ROWS', sum(r['PACKAGE_RELATIVE_FILE'].startswith('01_NUMERICAL_RESULTS/PAPER_I_II/') for r in origin_rows) == 16))
    checks.append(('PAPER_III_ORIGIN_ROWS', sum(r['PACKAGE_RELATIVE_FILE'].startswith('01_NUMERICAL_RESULTS/PAPER_III/') for r in origin_rows) == 24))
    checks.append(('PAPER_IV_ORIGIN_ROWS', sum(r['PACKAGE_RELATIVE_FILE'].startswith('01_NUMERICAL_RESULTS/PAPER_IV/') for r in origin_rows) == 37))
    checks.append(('FROZEN_CONTRACT_ORIGIN_ROWS', sum(r['PACKAGE_RELATIVE_FILE'].startswith('02_FROZEN_CONTRACTS/') for r in origin_rows) == 22))
    for row in origin_rows:
        package_file = ROOT / row['PACKAGE_RELATIVE_FILE']
        checks.append((f"ORIGIN_{row['PACKAGE_RELATIVE_FILE']}", package_file.is_file() and sha256(package_file) == row['SOURCE_SHA256'] == row['PACKAGE_SHA256']))

    forbidden_ext = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'}
    checks.append(('NO_IMAGE_FILES', not any(p.suffix.lower() in forbidden_ext for p in ROOT.rglob('*') if p.is_file())))
    checks.append(('NO_HOLDOUT30_DATA', not any('HOLDOUT30' in p.name.upper() for p in ROOT.rglob('*') if p.is_file())) )
    failed = [name for name, ok in checks if not ok]
    print('NUMERICAL_CHECK=' + ('PASS' if not failed else 'FAIL'))
    print('CHECKS=' + str(len(checks)))
    print('FAILED=' + (','.join(failed) if failed else 'NONE'))
    if failed:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
