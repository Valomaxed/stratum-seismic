"""Render the reviewer figure from the saved independent-verification report."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]


def main():
    report = json.loads((ROOT/'data/seismic-validation/report.json').read_text(encoding='utf8'))
    rows = [r for r in report['comparisons'] if r['case'] == 'el-centro-default-4-story']
    colors = ['#2563eb', '#c65b13', '#007f65']
    labels = ['Unbraced', 'X-braced', 'Chevron']
    values = [[1/r['frequencies_stratum_hz'][0] for r in rows],
              [r['peaks']['drift_pct']['stratum'] for r in rows],
              [r['peaks']['base_shear_kn']['stratum'] for r in rows]]
    plt.rcParams.update({'font.size': 10, 'axes.spines.top': False,
                         'axes.spines.right': False, 'savefig.facecolor': 'white'})
    fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.9))
    for ax, data, title, unit in zip(axes, values,
            ['First natural period', 'Peak interstory drift', 'Peak base-shear demand'],
            ['s', '%', 'kN']):
        bars = ax.bar(labels, data, color=colors, width=.6)
        ax.set(title=title, ylabel=unit, ylim=(0, max(data)*1.25))
        ax.bar_label(bars, fmt='%.3g', padding=4, fontsize=9)
        ax.grid(axis='y', alpha=.15)
        ax.set_axisbelow(True)
    fig.suptitle('Controlled elastic frame comparison · El Centro example · four stories', fontsize=12)
    fig.text(.5, .02, 'Same motion, geometry and prescribed floor masses; equal brace volume for X and chevron. One record, not a universal ranking.',
             ha='center', fontsize=8, color='#444444')
    fig.tight_layout(rect=(0, .05, 1, .92))
    path = ROOT/'data/seismic-validation/review-summary.png'
    fig.savefig(path, dpi=180)
    print(path)


if __name__ == '__main__':
    main()
