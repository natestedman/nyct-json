#!/usr/bin/env python

import json
import settings
import os
import urllib2
from proto import gtfs_realtime_pb2

message = gtfs_realtime_pb2.FeedMessage()
url = urllib2.urlopen('http://datamine.mta.info/mta_esi.php?key={0}&feed_id={1}'.format(settings.MTA_API_KEY, settings.MTA_FEED_ID))
message.ParseFromString(url.read())
url.close()

stops = {}

for entity in message.entity:
    if entity.trip_update.trip.route_id == "L":
        for stop_time_update in entity.trip_update.stop_time_update:
            stop_id = stop_time_update.stop_id
            
            if stop_id not in stops:
                stops[stop_id] = []
                
            stops[stop_id].append(stop_time_update.departure.time)

temp = os.path.join(settings.JSON_OUT_DIR, 'temp')

for stop_id, departures in stops.items():
    file = open(temp, 'w+')
    file.write(json.dumps(sorted(departures)))
    file.flush()
    os.fsync(file)
    file.close()
    
    os.rename(temp, os.path.join(settings.JSON_OUT_DIR, stop_id + ".json"))
