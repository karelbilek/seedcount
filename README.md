# seedcount
Utilities for counting letter coverage of random BIP39 mnemonics 

Introduction to the general problem
====

We have some set of two-sided cards with letters, on each card are two letters, one from each side. The cards are intended for writing down a BIP39 seed, 24 words.

We want to make as little cards as possible to cover as many possible BIP39 seeds as possible. An additional goal is make the number of the cards divisible by some number, for example 10, so that they could be manufactured more easily.

Words in BIP39 word list are constructed so that only first 4 letters suffice. (Space needs to be an actual letter.)

I assume only following set of cards (what's important to note that each letter is only one one type of card):

* a/e
* r/o
* i/s
* t/n
* l/c
* u/p
* d/m
* b/g
* h/f
* w/v
* k/y
* x/j
* z/q
* space 

By a greedy algorithm, I try to incrementally find out what is the best combination of cards for a given "card deck size", starting from smallest deck size and ending at 100% coverage, and print the deck plus its coverage.

It's hard, however, to compute this exactly (or, more exactly, I haven't found how); meaning, for a given set of cards, we can't compute how many possible seeds are covered. Also, for small deck sizes, it's usually close to 0%.

So, I compute the coverage by two means:

* naive approximate - I count a very rough approximate by counting exactly for every card separately, how big is the coverage of BIP39 seeds *for the given letters*
  * meaning - for how many seeds would this suffice, *only looking at this letter*
    * this is easy to count exactly and quickly by using memoization
  * then I am assuming independency of those and just multiply them
    * which is not correct, since `P((there is enough a/e) && (there is enough r/o)) = P(there is enough a/e)P(there is enough r/o | there is enough a/e)`, and `P(there is enough r/o)` and `P(there is enough a/e)` are not independent
* monte carlo approximate
  * I have pre-generated a set of 6 million seeds randomly and computed the coverage repeatedly on this set
  * coverage was computed by putting the counts into a PostgreSQL database and making SQL queries 

In this repo there is all you need to replicate those experiments. All are using python3.

Generating random seeds
====
First install pbkdf2

     sudo pip3 install pbkdf2

then run 
    
     ./generate_big.py > big

The script never ends, so you will either have to kill it by ctrl-c or just pipe it to `head` for a limited set

     ./generate_big.py | head -n 50

My results (slightly over 6 million seeds) can be found [here](https://dl.dropboxusercontent.com/u/12170550/counting/big_seeds.tar.xz) (279 MB zipped, 980MB unzipped).

Converting seeds to CSV with counts
=====

    cat bit | ./convert_seeds_to_csv.py > csv

Results for the same set of seeds can be found [here](https://dl.dropboxusercontent.com/u/12170550/counting/big_csv.tar.xz) (44 MB zipped, 206MB unzipped)

Create SQL from csv
====

First install postgres...

    sudo apt-get install postgresql postgresql-contrib

let's for simplicity just use postgresql user for everything

    sudo -u postgres createdb seedcountdb

and now create the tables. Note: user postgres must have access right to read the file.

    ./create_sql.py /path/to/csv postgres seedcountdb counttable

Do the greedy search
=====
Assuming the SQL table is created

    ./count_prob 10 postgres seedcountdb counttable
    
where 10 is the divisibility (it can be anything from 1 to infinity)

Final results
====

They are in final/ directory

