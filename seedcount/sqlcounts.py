#!/usr/bin/env python3

import subprocess

def run_sql(user, sql, db):
    system = "sudo -u "+user+" psql -d "+db+" -Atc '"+sql+"'"
    res = subprocess.check_output(system, shell=True)
    return res.decode().rstrip()     

word_count = 0

def count_word_count(user, db, table):
    return int(run_sql(user, "SELECT COUNT (*) FROM "+table, db))

def actual_prob(cards, user, db, table):
    global word_count

    if word_count == 0:
        word_count = count_word_count(user, db, table)

    sql = "SELECT COUNT (*) FROM "+table+" WHERE "
    sql += " AND ".join([
            '"'+double+'" <= '+"%d" % cards[double] 
            for double in cards.keys()
        ])

    c = int(run_sql(user, sql, db))
    return c/word_count

doubles = ["ae",
"ro",
"is",
"tn",
"lc",
"up",
"dm",
"bg",
"hf",
"wv",
"ky",
"xj",
"zq",
"_"]

def sql_create(user, db, table):
    sql = 'CREATE TABLE '+table+'(id  SERIAL, '
    sql += ", ".join(['"'+double+'" INT' for double in doubles] )
    sql += ");"
    for double in doubles:
        sql += 'CREATE INDEX ON '+table+' USING btree("'+double+'");'
    sql += 'CREATE INDEX ON '+table+' USING btree(' + ", ".join(['"'+double+'"' for double in doubles])+");"
    run_sql(user, sql, db)

def sql_copy(csv, user, db, table):
    sql = "COPY " + table + " ( " + ", ".join(['"' + double + '"' for double in doubles]) + ") FROM '" + csv + "' DELIMITER ',' CSV"
    run_sql(user, sql, db)

if __name__ == '__main__':
    #cards = {'tn': 20, 'ae': 20, 'zq': 10, 'xj': 10, '_': 10, 'ky': 10, 'is': 20, 'hf': 10, 'wv': 10, 'bg': 10, 'lc': 10, 'dm': 10, 'up': 10, 'ro': 20}
    #cards = {'tn': 20, 'ae': 30, 'zq': 10, 'xj': 10, '_': 10, 'ky': 10, 'is': 20, 'hf': 10, 'wv': 10, 'bg': 10, 'lc': 20, 'dm': 10, 'up': 20, 'ro': 20}
    cards =  {'ae': 17, 'lc': 10, 'zq': 1, '_': 2, 'ky': 3, 'hf': 5, 'is': 13, 'ro': 13, 'tn': 10, 'wv': 4, 'up': 8, 'dm': 7, 'bg': 5, 'xj': 1}
    print (actual_prob(cards, "postgres", "seedcount", "pocty"))
    #sql_create("whatever", "postgres", "seedcount", "pocty2")
