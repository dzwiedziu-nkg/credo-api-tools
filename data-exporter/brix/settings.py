import csv

DIR = 'credo-data-export/detections'
CSV = 'credo-data-export/credocut.tsv'
PLOT = 'credo-data-export/credocut.plot'
DEVICES = 'credo-data-export/device_mapping.json'
CREDOCUT = 10069

DELIMITER='\t'
QUOTECHAR='"'
QUOTING=csv.QUOTE_MINIMAL

COLUMNS = [
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
    'visible',
    'frame_content'
]

TSV_COLUMNS = {}
for i in range(0, len(COLUMNS)):
    TSV_COLUMNS[COLUMNS[i]] = i

BLACKLIST = set()
