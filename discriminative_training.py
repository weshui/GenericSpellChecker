import random
import numpy as np

from weblm import weblm_req

global dic_errormodel = {}


def score_function(s, q, errortype, para_l , para_u):
	'''Input correction s, query q, errortype list, parameter lambda and parameter u, calculate and return score'''
	score = para_u + para_u.get(errortype[0],0)* errormodel(s[0], q[0])
	for i in range(1, s.length()):
		if " " in s[i]:
			#Spliting state
			score += para_l * weblm_req(s[i-1],s[i])
			wilist = s[i].split(" ")
			for j in range(1,len(wilist)):
				score += para_l * weblm_req(wilist[j-1],wilist[j])
		elif(s[i] == "" or s[i]== None):
			#merging state
			if (len(s) - 1 >= i + 1):
				score += para_l * weblm_req(s[i+1],s[i-1])
		else:
			score += para_l * weblm_req(s[i-1], s[i])
			score += para_u.get(errortype[i],0) * errormodel(s[i],q[i]) 
 	return score
	
def errormodel(correction, query):
	'''Input correction and query return prob'''
	return random.random()


def discriminative_train(correction, query, errortype):	
	'''correction, query, errortype lists '''
	para_l = random.random()
	tmpu = [random.random() for i in range(4)]
	para_u = dict(zip(['0','1', '2', '3'], tmpu))
	max_iteration_num = 12
	para_l_list = []
	para_u_list = {'0':[], '1':[], '2':[], '3':[]}
	while iternum < max_iteration_num:
		iternum += 1 
		res_states, res_errortypes = algorithm_2(query, k, para_l, para_u)
		topone_state = res_states[0]
		topone_errortype = res_errortypes[0]
		if correction !=  topone :
			for i in range(len(query)):
				para_l = para_l + weblm_req(query[i], correction[i]) - weblm_req(query[i], topone_state[i])
				para_u[errortype[i]] = para_u[errortype[i]] + errormodel(correction[i], query[i])
				para_u[topone_errortype[i]] = para_u[topone_errortype[i]] - errormodel(topone_state[i], query[i])
			# append the params to the list
			para_l_list.append(para_l)
			for ek in para_u_list.keys():
				para_l_list[ek].append(para_u[ek])
		else:
			break
	f_para_l = np.mean(para_l_list)
	f_para_u = dict(zip(['0', '1', '2', '3']),[0,0,0,0]) 
	for ek in para_u_list.keys():
		f_para_u[ek] = np.mean(para_u_list[ek])
		
	return f_para_l, f_para_u
	
