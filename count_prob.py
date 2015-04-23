#!/usr/bin/env python3
from sys import argv
from seedcount import greedysearch


step = int(argv[1])
user = argv[2]
db = argv[3]
table = argv[4]

greedysearch.greedysearch(step, user, db, table)

