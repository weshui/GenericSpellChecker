#!/usr/bin/python
# Programmer : Shuomeng
# Date: 
# Last-modified: 07 Dec 2016 10:53:04 PM

import os,sys,argparse

def ParseArg():
    ''' This Function Parse the Argument '''
    p=argparse.ArgumentParser( description = 'Example: %(prog)s -h', epilog='Library dependency : pysam')
    p.add_argument('-v','--version',action='version',version='%(prog)s 0.1')
    if len(sys.argv) < 2:
        print p.print_help()
        exit(1)
    return p.parse_args()

import re
from collections import Counter

def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('big.txt').read()))

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word]/N

def correction(word): 
    "Most probable spelling correction for word."
    if len(word.split(" "))>1:
        wlist = word.split(" ")
        re = []
        for w in wlist:
            re.append(max(candidates(w),key=P))
        return " ".join(re)
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


#def g():
#    global big
#    big = file('big.txt').read()
#    N = len(big)
#    s = set()
#    for i in xrange(6, N):
#        c = big[i]
#        if ord(c) > 127 and c not in s:
#            print i, c, ord(c), big[max(0, i-10):min(N, i+10)]
#            s.add(c)
#    print s
#    print [ord(c) for c in s]


def Main(): 
    global args
    #args=ParseArg()
    #print >>sys.stderr,args
    print "smothing edit one", len(edits1('smothing'))
    print "correction ", correction('speling')
    
    
if __name__=="__main__":
    Main()

