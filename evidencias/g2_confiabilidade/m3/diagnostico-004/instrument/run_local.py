#!/usr/bin/env python3
"""Repeat M3 in the prepared local Docker environment, without official acceptance."""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import shlex
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--product', type=Path, default=REPO.parent / 'Projeto/i-educar-m3')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    output = args.output or REPO / 'evidencias/g2_confiabilidade/m3' / (
        'diagnostico-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    print('Evidências: ' + str(output), flush=True)
    return subprocess.call([
        sys.executable, str(HERE / 'run.py'), '--diagnostic',
        '--product', str(args.product), '--output', str(output),
        '--php-command', shlex.join(['bash', str(HERE / 'php.sh')]),
    ])


if __name__ == '__main__':
    raise SystemExit(main())
