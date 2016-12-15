import candidates
import sys

import random
import numpy as np
from difflib import SequenceMatcher
from weblm import weblm_req

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
				updated_corrections.append(corrections[i]+[None])
				updated_states.append(states[i]+[4])

		corrections = updated_corrections
		states = updated_states
	return (corrections, states)

def score_function(s, q, errortype, para_l , para_u):
	'''Input correction s, query q, errortype list, parameter lambda and parameter u, calculate and return score'''
	score = para_u[errortype[0]] + para_u[errortype[0]]* errormodel(s[0], q[0])
	for i in range(1, len(s)):
                print "i", i, s[i]
                if(s[i] == "" or s[i]== None):
			#merging state
			if (len(s) - 1 >= i + 1):
				score += para_l * weblm_req(s[i+1],s[i-1])
		        print "merging", score
		elif " " in s[i]:
			#Spliting state
			score += para_l * weblm_req(s[i-1],s[i])
			wilist = s[i].split(" ")
			for j in range(1,len(wilist)):
				score += para_l * weblm_req(wilist[j-1],wilist[j])
		        print "splitting", score
                else:
			score += para_l * weblm_req(s[i-1], s[i])
			score += para_u.get(errortype[i],'0') * errormodel(s[i],q[i]) 
 	                print "else score",score
        print "Test score function", s, q, errortype, para_l, para_u
        print "Final score",score
        return score
	
def errormodel(correction, query):
	'''Input correction and query return prob'''
	if correction == None or correction == "" or query == "" or query == None:
            print "error model", correction, query,"rate", 0
            return 0
        rs = SequenceMatcher(None, correction, query).ratio()
        print "error model", correction, query,"rate", rs
        return rs

#def algorithm_2(query, k, para_l, para_u):
#        return ([['government', None, 'homepage', 'f', 'illinois state']], [[0, 4, 2, 0, 3]])


def discriminative_train(correction, query, errortype):	
	'''correction, query, errortype lists '''
        #init parameter
	para_l = random.random()
	tmpu = [random.random() for i in range(5)]
	para_u = dict(zip([0,1, 2, 3, 4], tmpu))
        
        #init parameter list	
        para_l_list = []
	para_u_list = {0:[], 1:[], 2:[], 3:[], 4:[]}
	
        max_iteration_num = 3
	iternum = 0
	k = 3

	while iternum < max_iteration_num:
		iternum += 1 
		res_states, res_errortypes = algorithm_2(query, k, para_l, para_u)
		topone_state = res_states[0]
		topone_errortype = res_errortypes[0]
                print "itern:",iternum,"topone state",topone_state, "topone_errortype", topone_errortype
		if correction !=  topone_state :
			for i in range(len(query)):
                                para_l = para_l + weblm_req(query[i], correction[i]) - weblm_req(query[i], topone_state[i])
				para_u[errortype[i]] = para_u[errortype[i]] + errormodel(correction[i], query[i])
				para_u[topone_errortype[i]] = para_u[topone_errortype[i]] - errormodel(topone_state[i], query[i])
			# append the params to the list
			para_l_list.append(para_l)
			for ek in para_u_list.keys():
				para_u_list[ek].append(para_u[ek])
                        print "Now para_l",para_l, "para_u", para_u
		else:
			break
	
        print "param lists", para_l_list, para_u_list
        f_para_l = np.mean(para_l_list)
	f_para_u = dict(zip([0, 1, 2, 3, 4],[0,0,0,0,0])) 
        	
        for ek in para_u_list.keys():
		f_para_u[ek] = np.mean(para_u_list[ek])
	print "final trained params",f_para_l, f_para_u	
	return f_para_l, f_para_u



query = ['goverment','home', 'page','of', 'illinoisstate']
correction = ['government', None, 'homepage', 'of', 'illinois state']
correction2 = ['govermment', None, 'homepage', 'of', 'illinois state']
error_type = [0,4,2,0,3]

para_l, para_u = discriminative_train(correction, query, error_type)

print "Call score function"
score_function(correction, query,error_type, para_l, para_u)
score_function(correction2, query,error_type, para_l, para_u)



if __name__=="__main__":
	query = sys.argv[1]
	query = query.split()
	
	print algorithm_2(query, 2, 2, 2)
