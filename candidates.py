import sys


# Read in lexicon for testing purpose
def read_lexicon(path): 
	with open(path) as f:
	    words = f.read().splitlines()
	return dict((el,1) for el in words)


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

def edits3(word): 
	"All edits that are three edits away from `word`."
	return (e3 for e2 in edits2(word) for e3 in edits2(e2))

# Filter all candidates wiht in specified editdistacne 
# @ word: candidate words with in edit dissatacen generated from candidates()
# @ return: set of words with in edit distance that are also in the lexicon
def filter(words, lexicon): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in lexicon)

# Generate candidate and filter so that all candidates blong to lexicon
# @ word: target word to correct
# @ distance: number of edits from original word, allow only 1-3 for the purpose of refining search space
def candidates(word, distance, lexicon): 
    "Generate possible spelling corrections for word."
    if distance == 1:
    	return (filter([word], lexicon).union(filter(edits1(word), lexicon)))
    elif distance == 2:
    	return (filter([word], lexicon).union(filter(edits1(word), lexicon)).union(filter(edits2(word), lexicon)))


# For module testing purpose
# Not used in integrated framework
if __name__ == "__main__": 
	target = sys.argv[1]
	distance = int(sys.argv[2])
	lexicon = read_lexicon("file.txt")
	candidate = candidates(target, distance, lexicon)
	print candidate
