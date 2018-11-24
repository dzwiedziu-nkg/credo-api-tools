from os import listdir
from os.path import join

import ijson

from brix.settings import *


csv_file = open(CSV, 'w')
writer = csv.writer(csv_file, delimiter=DELIMITER, quotechar=QUOTECHAR, quoting=QUOTING)
writer.writerow(COLUMNS)

jsons = [f for f in listdir(DIR) if f.endswith('.json')]

i = 0
count = len(jsons)

for fn in sorted(jsons):
    i += 1
    print('Open file: %s (%d of %d)...' % (fn, i, count))

    f = join(DIR, fn)
    with open(f, 'r') as json:
        objects = ijson.items(json, 'detections.item')

        j = 0

        for o in objects:
            j += 1
            if j % 10000 == 0:
                print('...processed %d hits' % j)

            user_id = o.get('user_id')
            if int(user_id) != CREDOCUT:
                continue
            row = []
            for c in COLUMNS:
                row.append(o.get(c))
            writer.writerow(row)

            print('...save BRIX hit from %d device' % o.get('device_id'))
        print('...finish of %s, processed %d hits' % (fn, j))

csv_file.close()
