from os import mkdir

from os.path import join, isdir

import base64
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

minutes = {}

for row in reader:
    if row[0] == 'id':
        continue

    rid = int(row[0])
    if rid in BLACKLIST:
        continue

    hid = int(row[TSV_COLUMNS['id']])
    device_id = int(row[TSV_COLUMNS['device_id']])
    timestamp = int(row[TSV_COLUMNS['timestamp']])
    frame_content = row[TSV_COLUMNS['frame_content']]

    if device_id in devices:
        nr = devices.get(device_id)
    else:
        nr = len(devices.keys()) + 1
        devices[device_id] = nr
        rdevices[nr] = device_id

    plot = data.get(nr, {
        'x': [],
        'y': [],
        'hit': [],
        'type': 'scatter',
        'mode': 'markers',
        'name': devs.get(device_id).get('device_model')
    })

    plot['x'].append(timestamp)
    plot['y'].append(1 + nr * 0.025)
    plot['hit'].append(hid)
    data[nr] = plot

    minute = timestamp // 60000
    minutes[minute] = minutes.get(minute, 0) + 1

    if not isdir(PNG):
        mkdir(PNG)
    f = open(join(PNG, '%d.png' % hid), 'wb')
    f.write(base64.b64decode(frame_content))
    f.close()


plot_minutes = {
    'x': [],
    'y': [],
    'type': 'scatter',
    'mode': 'markers',
    'name': 'In minute'
}

for m in minutes.keys():
    v = minutes.get(m)
    if v > 1:
        plot_minutes['x'].append(m * 60000 + 30000)
        plot_minutes['y'].append(v)

plots = [plot_minutes]
for d in range(1, len(devices) + 1):
    plots.append(data[d])

with open(JSON, 'w') as f:
  json.dump({'plots': plots}, f, ensure_ascii=False)
