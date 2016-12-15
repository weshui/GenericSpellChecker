import random
import numpy as np
from difflib import SequenceMatcher
from weblm import weblm_req
from errormodel import errormodel

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
	
	'''Input correction and query return prob'''
	if correction == None or correction == "" or query == "" or query == None:
            print "error model", correction, query,"rate", 0
            return 0
        rs = SequenceMatcher(None, correction, query).ratio()
        print "error model", correction, query,"rate", rs
        return rs



