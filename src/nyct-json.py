#!/usr/bin/env python

import json
import settings
import os
import urllib2
from proto import gtfs_realtime_pb2

# download MTA data
message = gtfs_realtime_pb2.FeedMessage()
url = urllib2.urlopen('http://datamine.mta.info/mta_esi.php?key={0}&feed_id={1}'.format(settings.MTA_API_KEY, settings.MTA_FEED_ID))
message.ParseFromString(url.read())
url.close()

# find all departure times and arrange by station
stops = {}

for entity in message.entity:
    if entity.trip_update.trip.route_id == "L":
        for stop_time_update in entity.trip_update.stop_time_update:
            # find stop identifier and direction
            stop_id = stop_time_update.stop_id
            prefix = stop_id[:-1]
            direction = stop_id[-1:]
            
            # insert empty lists
            if prefix not in stops:
                stops[prefix] = { 'N': [], 'S': [] }
            
            # add current departure time
            stops[prefix][direction].append(stop_time_update.departure.time)

# sort departure times
for stop_id in stops:
    for direction in stops[stop_id]:
        stops[stop_id][direction].sort()

# write JSON
temp = os.path.join(settings.JSON_OUT_DIR, 'temp')

def write(filename, json_representation):
    file = open(temp, 'w+')
    file.write(json.dumps(json_representation))
    file.flush()
    os.fsync(file)
    file.close()
    
    os.rename(temp, filename)

for stop_id, directions in stops.items():
    write(os.path.join(settings.JSON_OUT_DIR, stop_id + ".json"), directions)
    
    for direction, departures in directions.items():
        write(os.path.join(settings.JSON_OUT_DIR, stop_id + direction + ".json"), departures)
