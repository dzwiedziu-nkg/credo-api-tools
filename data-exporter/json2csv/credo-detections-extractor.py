import argparse
from sys import stdin, stdout, stderr
import csv
import base64
import os
import os.path
import datetime

import ijson


def prepare_args():
    parser = argparse.ArgumentParser(
        description="Tool export PNG files and detection data to CSV.",
        usage="./credo-user-mapping.py -j export_0_1526045901710.json -c detecions.csv -p png/",
        epilog="Author: Michał Niedźwiecki, Cracow University of Technology"
    )

    parser.add_argument("--json", "-j", help="Path to JSON file with detections or '-' for stdin", required=True)
    parser.add_argument("--csv", "-c", help="Output of CSV file or '-' for stdout")
    parser.add_argument("--png", "-p", help="Path to directory where PNG files will be store, "
                                            "when you no provide the path then PNG files will not be stored")
    parser.add_argument("--base64", "-b", help="Write encoded PNG file in CSV row", action='store_true')
    #parser.add_argument("--append", "-a", help="Write encoded PNG file in CSV row", action='store_true')
    parser.add_argument("--delimiter", help="CSV delimiter", default="\t")
    parser.add_argument("--quotechar", help="CSV quotechar", default='"')
    parser.add_argument("--quoting", help="CSV quoting: 0 - minimal, 1 - all, 2 - none, 3 - nonnumeric", default='0')

    return parser.parse_args()


def export(json_file, csv_file, args):
    lines = 0

    hot_pixels = {}

    objects = ijson.items(json_file, 'detections.item')
    if csv_file:
        writer = csv.writer(csv_file, delimiter=args.delimiter, quotechar=args.quotechar, quoting=int(args.quoting))

        columns = [
            'id',
            'user_id',
            'device_id',
            'team_id',
            'width',
            'height',
            'x',
            'y',
            'latitude',
            'longitude',
            'altitude',
            'accuracy',
            'provider',
            'source',
            'time_received',
            'timestamp',
            'visible'
        ]

        if False: #not args.append:
            writer.writerow(columns)

        if args.base64:
            columns.append('frame_content')

    counts = {}
    to_write = dict()
    for o in objects:
        device_id = o.get('device_id') or 0

        hp_key = '%d_%d_%d' % (
            o.get('device_id') or 0,
            o.get('x') or 0,
            o.get('y') or 0
        )

        tw_key = '%s_%d' % (hp_key, o.get('timestamp') or 0)

        x = o.get('x')
        hp = None
        if x is not None:
            hp = hot_pixels.get(hp_key)

        if hp is not None:
            try:
                to_write.pop(tw_key)
                counts[device_id] = counts.get(device_id, 0) - 1
            except:
                pass
        else:
            counts[device_id] = counts.get(device_id, 0) + 1
            to_write[tw_key] = o
            hot_pixels[hp_key] = True

    for k in to_write.keys():
        o = to_write[k]
        lines += 1
        device_id = o.get('device_id') or 0

        if csv_file:
            values = list(map(lambda c: o[c], columns))
            writer.writerow(values)
        if args.png:
            frame = base64.b64decode(o.get('frame_content'))

            epoch = datetime.datetime.utcfromtimestamp((o.get('timestamp') or 0) / 1000)
            dt = epoch.strftime("%Y_%m_%d__%H_%M_%S_%f")

            fn = '%s/%05d_%05d_%s_%04d_%04d_%04d_%04d_%04d.png' % (
                args.png,
                counts[device_id],
                device_id,
                dt,
                o.get('user_id') or 0,
                o.get('width') or 0,
                o.get('height') or 0,
                o.get('x') or 0,
                o.get('y') or 0
            )

            if counts[device_id] > 400:
                print('Skipping file: %s' % fn)
            else:
                print('Writing file: %s' % fn)

                f = open(fn, 'wb')
                f.write(frame)
                f.close()

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
    elif args.csv:
        print('Writing CSV to %s' % args.csv, file=stderr)
        cf = open(args.csv, 'w')
    else:
        cf = None

    if args.png:
        try:
            os.mkdir(args.png)
        except:
            pass

    print('Using settings:', file=stderr)
    print('  PNG in CSV row: %s' % ("yes" if args.base64 else "no"), file=stderr)
    if args.delimiter == '\t':
        print('  delimiter=(tabulator)', file=stderr)
    else:
        print('  delimiter=%s' % args.delimiter, file=stderr)
    print('  quotechar=%s' % args.quotechar, file=stderr)
    print('  quoting=%s' % args.quoting, file=stderr)

    lines = export(jf, cf, args)

    if jf != stdin:
        jf.close()

    if cf and cf != stdout:
        cf.close()

    print('Done, exported: %d lines' % lines, file=stderr)


if __name__ == "__main__":
    main(prepare_args())




"""
6679
4143
1276
6399
6300
6363
5679
6288
5847
5035
"""
