import ijson

from brix.settings import DEVICES


def load_devices(ids: set = None, file: str = DEVICES):
    ret = {}

    with open(file, 'r') as json:
        objects = ijson.items(json, 'devices.item')
        for o in objects:
            did = int(o.get('id'))
            if ids is None or did in ids:
                ret[did] = o

    return ret
