########### Python 2.7 #############
import httplib, urllib, base64, json

def weblm_req(prevstr, cword):
	'''Input previous str and current word list, call webLM API to get the conditional probability'''
	
	#Request body
	body = {}
	body['queries'] = []
	body['queries'].append({"words":prevstr,"word":cword})	
        
        if prevstr == None or prevstr == "" or cword == None or cword == "" :
            return 0

	headers = {
    	# Request headers
    	'Content-Type': 'application/json',
    	'Ocp-Apim-Subscription-Key': '8d8fda56b4ec4f4aa0ce85ff1aaf6a6c',
	}

	params = urllib.urlencode({
    	# Request parameters
    	'model': 'title',
    	'order': '2',
	})

	try:
    		conn = httplib.HTTPSConnection('api.projectoxford.ai')
    		conn.request("POST", "/text/weblm/v1.0/calculateConditionalProbability?%s" % params, json.dumps(body), headers)
    		response = conn.getresponse()
    		data = response.read()
    		#print "weblmresponse", data
    		res = json.loads(data)
                conn.close()
		return res["results"][0]["probability"]
	except Exception as e:
    		print "error",str(e), e
                return 0
#Example
# 	weblm_req("hello world wide", ['web','range','open'])
#	return and print 
#	{"results":[{"words":"hello world wide","word":"web","probability":-3.334},{"words":"hello world wide","word":"range","probability":-3.928},{"words":"hello world wide","word":"open","probability":-3.59}]}
