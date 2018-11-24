from datetime import datetime

from brix.devices import load_devices
from brix.settings import *


csv_file = open(CSV, 'r')
reader = csv.reader(csv_file, delimiter=DELIMITER, quotechar=QUOTECHAR, quoting=QUOTING)
writer = open(PLOT, 'w')

devices = {}
rdevices = {}

for row in reader:
    if row[0] == 'id':
        continue

    rid = int(row[0])
    if rid in BLACKLIST:
        continue

    device_id = int(row[TSV_COLUMNS['device_id']])
    timestamp = int(row[TSV_COLUMNS['timestamp']])

    if device_id in devices:
        nr = devices.get(device_id)
    else:
        nr = len(devices.keys()) + 1
        devices[device_id] = nr
        rdevices[nr] = device_id

    dt = datetime.fromtimestamp(timestamp / 1000)
    dtf = dt.strftime('%Y-%m-%d_%H:%M:%S')  # + '.%03d' % (dt.microsecond / 1000)
    writer.write('%s\t%d\t# %d\n' % (dtf, nr, device_id))

devs = load_devices(set(devices.keys()))
writer.write('# Device mapping:\n')
for d in range(1, len(devices) + 1):
    device_id = rdevices[d]
    device_model = devs.get(device_id).get('device_model')
    system_version = devs.get(device_id).get('system_version')
    writer.write("# %2d = %s, %s\n" % (d, device_model, system_version))
writer.close()
