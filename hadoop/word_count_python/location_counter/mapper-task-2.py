#!/usr/bin/env python3
"""mapper-task-2.py"""

import sys

# input comes from STDIN (standard input)
# write some useful code here and print to STDOUT

first_line = True

for line in sys.stdin:
    # if first_line:
    #     first_line = False
    #     continue  # Skip the header row

    columns = line.strip().split(',')
    location = columns[3]
    print("%s\t1" % location)
