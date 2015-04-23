#!/usr/bin/env python3
def start_from_word(word):
    word = word.rstrip()
    res = word[0:4]
    while len(res) < 4:
        res = res + "_"
    return res

def starts_from_seed(seed):
    seed = seed.rstrip()
    words = seed.split(" ")
    starts = [start_from_word(word) for word in words]
    return starts
 
