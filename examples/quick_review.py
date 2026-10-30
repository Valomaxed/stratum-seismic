"""Reproduce the default three-frame comparison without a web server.

Run from the repository root: python examples/quick_review.py
"""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from seismic_frame.model import compare


def run():
    record = ROOT/'web/records/el-centro-1940.at2'
    result = compare({'record': {'text': record.read_text(encoding='utf8'),
                                 'unit': 'g', 'name': 'El Centro 1940 NS, Peknold example'},
                      'scale_factor': 1.})
    keys = ('label', 'period_s', 'peak_drift_pct', 'peak_roof_mm',
            'peak_base_shear_kn', 'brace_volume_m3')
    return {'example': 'Controlled elastic response comparison', 'frame': result['frame'],
            'record': {k: result['record'][k] for k in
                       ('name', 'sha256', 'npts', 'dt', 'duration_s', 'scaled_pga_g')},
            'rows': [{k: system[k] for k in keys} for system in result['systems']],
            'scope': 'One attributed example record; these results are not a general ranking of bracing systems.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='Optional JSON result path')
    args = parser.parse_args()
    text = json.dumps(run(), indent=2, allow_nan=False)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding='utf8')
    print(text, end='')


if __name__ == '__main__':
    main()
