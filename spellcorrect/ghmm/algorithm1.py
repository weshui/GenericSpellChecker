import random
import numpy as np
from difflib import SequenceMatcher
from weblm import weblm_req
from errormodel import errormodel
from algorithm2 import algorithm_2

def discriminative_train(corrections, queries, errortypes):	
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
        
        for eci in range(len(corrections)):
            correction = corrections[eci]
            query = queries[eci]
            errortype = errortypes[eci]
            iternum = 0
	    while iternum < max_iteration_num:
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
                    if iternum == 0:
			para_l_list.append(para_l)
			for ek in para_u_list.keys():
				para_u_list[ek].append(para_u[ek])
                        
		    break 
	        iternum += 1 
        print "param lists", para_l_list, para_u_list
        f_para_l = np.mean(para_l_list)
	f_para_u = dict(zip([0, 1, 2, 3, 4],[0,0,0,0,0])) 
        	
        for ek in para_u_list.keys():
	    f_para_u[ek] = np.mean(para_u_list[ek])
	print "final trained params",f_para_l, f_para_u	
	
        return f_para_l, f_para_u


correction = [["a", "cat", "sat on","mat"]]
query = [["a", "bat", "saton","mat"]]
errortype = [[1,0,2,1]]

discriminative_train(correction,query,errortype)
