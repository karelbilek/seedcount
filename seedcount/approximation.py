#!/usr/bin/env python3
from functools import lru_cache
from seedcount import start

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


#in how many words is (first index) exactly (2nd index)-times
reverse_count = {double:{i:0 for i in range(0,5)} for double in doubles}


with open("english.txt") as words:
    for word in words:
        startt = start.start_from_word(word)
        for double in doubles:
            countdouble = 0
            for letter in startt:
                if letter in double:
                    countdouble+=1
            reverse_count[double][countdouble]+=1


#what is the probability that in WORDS we will have exactly EXACT-times the double-letter LETTER
#(this is exact and not approximation)
@lru_cache(maxsize=10000)
def _exact_prob(words, exact, letter):
    if (words == 1):
        if (exact > 4):
            return 0
        if (exact < 0):
            return 0
        return (reverse_count[letter][exact]/2048.0)
    else:
        sumprob = 0.0
        for missing in range(0,5):
            sumprob += _exact_prob(1, missing, letter) * _exact_prob(words-1, exact-missing, letter)
        return sumprob

#what is the probability that in WORDS we will have COUNT-times or less the double-letter LETTER
#(meaning, COUNT cards will be enough)
@lru_cache(maxsize=10000)
def _less_prob(words, count, letter):
    sumprob = 0.0
    for exact in range(0, count+1):
        sumprob += _exact_prob(words, exact, letter)
    return sumprob

#approximate (incorrect) probability that a given cards are enough
#incorrect, because it assumes that it's independent for all letters
#while it's actually very dependent
#....but the real probability is sometimes 0, so here at least I have a number
def approx_prob(cards):
    sumprob = 1.0
    for (double, count) in cards.items():
        sumprob *= _less_prob(24, count, double) #this multiplication incorrectly implies independency
    return sumprob


if __name__ == '__main__':
    cards = {'tn': 20, 'ae': 20, 'zq': 10, 'xj': 10, '_': 10, 'ky': 10, 'is': 20, 'hf': 10, 'wv': 10, 'bg': 10, 'lc': 10, 'dm': 10, 'up': 10, 'ro': 20}
    print (approx_prob(cards))
