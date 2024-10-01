#!/usr/bin/env python3
"""reducer-task-2.py"""

# input comes from STDIN (standard input)
# write some useful code here and print to STDOUT

import sys

locationMap = {}

for line in sys.stdin:
    line = line.strip()
    location, count = line.split('\t')
    try:
        count = int(count)
        locationMap[location] = locationMap.get(location, 0) + count
    except ValueError:
        pass

for location, count in locationMap.items():
    if(location == 'Location'):
        continue
    print ('%s\t%s'% (location, count))