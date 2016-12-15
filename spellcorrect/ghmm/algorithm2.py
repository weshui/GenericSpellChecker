import candidates
import sys
from score import score_function
import random

#Read lexicon and store as a dictionary
def read_lexicon(path): 
	with open(path) as f:
	    words = f.read().splitlines()
	return dict((el,1) for el in words)


# Check if the word can be splitted into two words
# return the splitted string if such 
def check_split(word, lexicon): 
	for i in range(1, len(word)): 
		if (lexicon.get(word[:i]) != None) and (lexicon.get(word[i:]) != None): 
			return word[:i]+" "+word[i:]
	return None

# Algorithm_2 in ghmm for query correction paper
# gnerate candidates based on edit distance and return the top k corrections based on scoring funciton
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
def algorithm_2(query, k, _la, _mu,lexicon):
	corrections = [[]]
	states = [[]]
	#for m in range(len(query)): 
	for m in range(len(query)):
		# transformation or split
		if lexicon.get(query[m]) == None: 
			split = check_split(query[m], lexicon)
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


		# Combine each candidate, and filter the corrections ranked lower than k 
		updated_corrections = []
		updated_states = []
		for i in range(len(corrections)):
			# if merging case
			if len(corrections[i])>0 and corrections[i][-1] == None: 
				merge = query[m-1] + candidate_words[0]
				if(lexicon.get(merge)!=None):
					updated_correction = corrections[i] + [merge]
					updated_corrections.append(updated_correction)
					updated_state = states[i] + [2]
					updated_states.append(updated_state)
			# if other case 
			else: 
				for j in range(len(candidate_words)):
					updated_correction = corrections[i] + [candidate_words[j]]
					updated_corrections.append(updated_correction)
					updated_state = states[i] + [error_type[j]]
					updated_states.append(updated_state)
                                if m < len(query)-1:
				    updated_corrections.append(corrections[i]+[None])
				    updated_states.append(states[i]+[4])

		#update correcions at end of each iteration
		corrections = updated_corrections
		states = updated_states
	
		# Sorting the top k candidates 
        scorelist = []
        for i in range(len(corrections)):
            scorelist.append(score_function(corrections[i], query, states[i], _la , _mu))
        sorted_idx = [x for (y,x) in sorted(zip(scorelist,range(len(corrections))), reverse=True )]
        
        topi = 1
        for si in sorted_idx[0:min(k, len(corrections))]:
            print topi, scorelist[si], corrections[si], states[si]
            topi += 1

        return ([corrections[sorted_idx[0]]], [states[sorted_idx[0]]])


if __name__=="__main__":
	query = sys.argv[1]
	k = int(sys.argv[2])
	lexicon = read_lexicon(sys.argv[3])
	query = query.split()
	tmp = [random.random() for i in range(5)]
	para_u = dict(zip(range(5),tmp))
	algorithm_2(query, k, 2, para_u, lexicon)





