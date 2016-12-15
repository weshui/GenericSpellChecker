import candidates
import sys
from score import score_function
import random

#Read lexicon and store as a dictionary
def read_lexicon(path): 
	with open(path) as f:
	    words = f.read().splitlines()
	return dict((el,1) for el in words)


lexicon = read_lexicon("file.txt")

def check_split(word): 
	print lexicon
	
	for i in range(1, len(word)): 
		if (lexicon.get(word[:i]) != None) and (lexicon.get(word[i:]) != None): 
			return word[:i]+" "+word[i:]
	return None

# Algorithm_2 in ghmm for query correction paper
# generate max top k candidate with each word within edit distance
# @query - list of query words
# @k - max number of returned correction queries
# @_la - lambda for scoring function
# @_mu - list of mu for scoring function
# @lexicon - all leagal words
# 0 - transformation
# 1 - misuse
# 2 - merging 
# 3 - splitting
def algorithm_2(query, k, _la, _mu):
	corrections = [[]]
	states = [[]]
	#for m in range(len(query)): 
	for m in range(len(query)):
		# transformation or split
		if lexicon.get(query[m]) == None: 
			split = check_split(query[m])
			# transformation
			if split == None:
				candidate_words = list(candidates.candidates(query[m], 2, lexicon))
				error_type = [0]*len(candidate_words)
			# split
			else: 
				candidate_words = [split]
				error_type = [3]

		else: #misuse or merging
			candidate_words = list(candidates.candidates(query[m],2, lexicon))
			error_type = [1]*len(candidate_words)


		updated_corrections = []
		updated_states = []
		for i in range(len(corrections)):

			if len(corrections[i])>0 and corrections[i][-1] == None: 
				merge = query[m-1] + candidate_words[0]
				if(lexicon.get(merge)!=None):
					updated_correction = corrections[i] + [merge]
					updated_corrections.append(updated_correction)
					updated_state = states[i] + [2]
					updated_states.append(updated_state)
			else: 
				for j in range(len(candidate_words)):
					updated_correction = corrections[i] + [candidate_words[j]]
					updated_corrections.append(updated_correction)
					updated_state = states[i] + [error_type[j]]
					updated_states.append(updated_state)
                                if m < len(query)-1:
				    updated_corrections.append(corrections[i]+[None])
				    updated_states.append(states[i]+[4])

		corrections = updated_corrections
		states = updated_states
	
        scorelist = []
        for i in range(len(corrections)):
            scorelist.append(score_function(corrections[i], query, states[i], _la , _mu))
        sorted_idx = [x for (y,x) in sorted(zip(scorelist,range(len(corrections))), reverse=True )]
        
        #print "print sorted_idx, corrections, states, scorelist", sorted_idx, corrections, states, scorelist
        topi = 1
        for si in sorted_idx[0:k]:
            print topi, scorelist[si], corrections[si], states[si]
            topi += 1

        #print "top3", corrections[sorted_idx[0:3]], states[sorted_idx[0:3]], scorelist[sorted_idx[0:3]]
        return ([corrections[sorted_idx[0]]], [states[sorted_idx[0]]])


if __name__=="__main__":
	query = sys.argv[1]
	query = query.split()
	tmp = [random.random() for i in range(5)]
        para_u = dict(zip(range(5),tmp))
        print "para+U", para_u, query
	print algorithm_2(query, 5, 2, para_u)





