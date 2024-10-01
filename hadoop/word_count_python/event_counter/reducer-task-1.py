#!/usr/bin/env python3
"""reducer.py"""

# input comes from STDIN (standard input)
# write some useful code here and print to STDOUT

import sys

eventTypeMap = {}

for line in sys.stdin:
    line = line.strip()
    eventType, count = line.split('\t')
    try:
        count = int(count)
        eventTypeMap[eventType] = eventTypeMap.get(eventType, 0) + count
    except ValueError:
        pass

for eventType, count in eventTypeMap.items():
    if(eventType == 'EventType'):
        continue
    print ('%s\t%s'% (eventType, count))