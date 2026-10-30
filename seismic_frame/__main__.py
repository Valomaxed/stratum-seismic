"""Command line entry point for local analysis and independent verification."""
import argparse
import json


def main():
    parser = argparse.ArgumentParser(description='STRATUM Seismic frame analysis')
    commands = parser.add_subparsers(dest='command', required=True)
    server = commands.add_parser('serve', help='Start the local seismic workspace')
    server.add_argument('--host', default='127.0.0.1')
    server.add_argument('--port', type=int, default=8767)
    verify = commands.add_parser('verify', help='Compare with independent OpenSees models')
    verify.add_argument('--opensees-python', required=True)
    verify.add_argument('--no-figures', action='store_true')
    args = parser.parse_args()
    if args.command == 'serve':
        from .server import serve
        serve(args.host, args.port)
    else:
        from .benchmark import run
        report = run(args.opensees_python, make_figures=not args.no_figures)
        print(json.dumps({'passed': report['passed'], 'report': 'data/seismic-validation/report.md'}))
        if not report['passed']:
            raise SystemExit(1)


if __name__ == '__main__':
    main()
