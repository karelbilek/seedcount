#!/usr/bin/env python3
from sys import argv
from seedcount import sqlcounts



path = argv[1]
user = argv[2]
db = argv[3]
table = argv[4]

sql_create(user, db, table)
sql_copy(path, user, db, table)


