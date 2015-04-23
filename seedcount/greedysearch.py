#!/usr/bin/env python3

import sqlcounts
import approximation
import sys
from copy import copy

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

def count_letters(cards):
    return sum(cards.values())


def next_state(state, step, user, db, table):
    prob = sqlcounts.actual_prob(state, user, db, table)
    using_actual = True
    #if "actual probability" is 0, use approximation for greedy search
    if (prob == 0):
        using_actual = False
        prob = approximation.approx_prob(state)
    results = {}
    for double in doubles:
        copystate = copy(state)
        copystate[double] += step
        if (using_actual):
            results[double] = sqlcounts.actual_prob(copystate, user, db, table)
        else:
            results[double] = approximation.approx_prob(copystate)
    best = list(reversed(sorted(results, key=results.get)))[0]
    copystate = copy(state)
    copystate[best]+=step;
    return copystate
 

def greedysearch(step, user, db, table):
    cards = {i:0 for i in doubles}
    prb = 0
    while ("%1.6g" % (100 * prb)) != "100":
    #while (count_state_letters(cards) < 500):
        prb = sqlcounts.actual_prob(cards, user, db, table)
        if (prb > 0):
            print("%d\t%1.6g %%\t%s" % (count_letters(cards), 100*prb, cards))
        print(count_letters(cards), file=sys.stderr)
        cards = next_state(cards, step, user, db, table)

if __name__ == '__main__':
    greedysearch(10, "postgres", "seedcount", "pocty")
