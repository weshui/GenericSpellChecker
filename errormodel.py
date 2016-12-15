import random
import numpy as np
from difflib import SequenceMatcher
from weblm import weblm_req

	
def errormodel(correction, query):
	'''Input correction and query return prob'''
	if correction == None or correction == "" or query == "" or query == None:
            print "error model", correction, query,"rate", 0
            return 0
        rs = SequenceMatcher(None, correction, query).ratio()
        print "error model", correction, query,"rate", rs
        return rs

