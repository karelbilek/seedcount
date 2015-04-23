#!/usr/bin/env python3
import sys
from seedcount import csv

for seed in sys.stdin:
    print (csv.csv_from_seed(seed))
