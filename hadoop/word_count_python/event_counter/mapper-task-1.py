#!/usr/bin/env python3
"""mapper.py"""

import sys

# input comes from STDIN (standard input)
# write some useful code here and print to STDOUT

first_line = True  # Flag to skip the first line (header)

for line in sys.stdin:
    # if first_line:
    #     first_line = False
    #     continue  # Skip the header row
    columns = line.strip().split(',')
    event_type = columns[1]
    print("%s\t1" % event_type)