import argparse
from sys import stdin, stdout, stderr
import csv

import ijson


def prepare_args():
    parser = argparse.ArgumentParser(
        description="Tool for convert a large user_mapping.json file to CSV.",
        usage="./credo-user-mapping.py -j user_mapping.json -c user_mapping.csv",
        epilog="Author: Michał Niedźwiecki, Cracow University of Technology"
    )

    parser.add_argument("--json", "-j", help="Path to user_mapping.json or '-' for stdin", required=True)
    parser.add_argument("--csv", "-c", help="Output of CSV file or '-' for stdout", required=True)
    parser.add_argument("--delimiter", help="CSV delimiter", default="\t")
    parser.add_argument("--quotechar", help="CSV quotechar", default='"')
    parser.add_argument("--quoting", help="CSV quoting: 0 - minimal, 1 - all, 2 - none, 3 - nonnumeric", default='0')

    return parser.parse_args()


def export(json_file, csv_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL):
    objects = ijson.items(json_file, 'devices.item')
    writer = csv.writer(csv_file, delimiter=delimiter, quotechar=quotechar, quoting=quoting)
    writer.writerow(['id', 'user_id', 'device_model', 'system_version', 'device_type'])
    lines = 0
    for o in objects:
        writer.writerow([o['id'], o['user_id'], o['device_model'], o['system_version'], o['device_type']])
        lines += 1
    return lines


def main(args):
    if args.json == '-':
        print('Reading JSON from stdin', file=stderr)
        jf = stdin
    else:
        print('Reading JSON from %s' % args.json, file=stderr)
        jf = open(args.json, 'r')

    if args.csv == '-':
        print('Writing CSV to stdout', file=stderr)
        cf = stdout
    else:
        print('Writing CSV to %s' % args.csv, file=stderr)
        cf = open(args.csv, 'w')

    print('Using settings:', file=stderr)
    if args.delimiter == '\t':
        print('  delimiter=(tabulator)', file=stderr)
    else:
        print('  delimiter=%s' % args.delimiter, file=stderr)
    print('  quotechar=%s' % args.quotechar, file=stderr)
    print('  quoting=%s' % args.quoting, file=stderr)

    lines = export(jf, cf, delimiter=args.delimiter, quotechar=args.quotechar, quoting=int(args.quoting))

    if jf != stdin:
        jf.close()

    if cf != stdout:
        cf.close()

    print('Done, exported: %d lines' % lines, file=stderr)


if __name__ == "__main__":
    main(prepare_args())
