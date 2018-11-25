import json

from brix.devices import load_devices
from brix.settings import *


csv_file = open(CSV, 'r')
reader = csv.reader(csv_file, delimiter=DELIMITER, quotechar=QUOTECHAR, quoting=QUOTING)
json_data = {'x': [], 'y': [], 'devices': {}}

devices = {}
rdevices = {}

data = {}

devs = load_devices()

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

    plot = data.get(nr, {
        'x': [],
        'y': [],
        'type': 'scatter',
        'mode': 'markers',
        'name': devs.get(device_id).get('device_model')
    })

    plot.get('x').append(timestamp)
    plot.get('y').append(1)
    data[nr] = plot

#devs = load_devices(set(devices.keys()))
#for d in range(1, len(devices) + 1):
#    device_id = rdevices[d]
#    json_data.get('devices')[d] = devs.get(device_id)

plots = []
for d in range(1, len(devices) + 1):
    plots.append(data[d])

with open(JSON, 'w') as f:
  json.dump({'plots': plots}, f, ensure_ascii=False)
