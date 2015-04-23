#!/usr/bin/env python3
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

#c



backdoubles = {letter:double for double in doubles for letter in double}


def count_from_starts(starts):

    counts = {double:sum(
            [1 for word in starts for letter in word if double==backdoubles[letter]]
    ) for double in doubles}
    return counts


def csv_from_starts(starts):
    counts = count_from_starts(starts)
    res = ",".join([str(counts[double]) for double in doubles])
    return res
    
def count_from_seed(seed):
    return count_from_starts(start.starts_from_seed(seed))

def csv_from_seed(seed):
    return csv_from_starts(start.starts_from_seed(seed))


if __name__ == '__main__':
    import generate
    seed = generate.generate()
    print(seed)
    print( start.starts_from_seed(seed))
    print( csv_from_seed(seed))
