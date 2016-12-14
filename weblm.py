########### Python 2.7 #############
import httplib, urllib, base64, json

def weblm_req(prevstr, cwords):
	'''Input previous str and current word list, call webLM API to get the conditional probability'''
	
	#Request body
	body = {}
	body['queries'] = []
	for word in cwords:
		body['queries'].append({"words":prevstr,"word":word})	

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
    		print(data)
    		conn.close()
		return data
	except Exception as e:
    		print("[Errno {0}] {1}".format(e.errno, e.strerror))

#Example
# 	weblm_req("hello world wide", ['web','range','open'])
#	return and print 
#	{"results":[{"words":"hello world wide","word":"web","probability":-3.334},{"words":"hello world wide","word":"range","probability":-3.928},{"words":"hello world wide","word":"open","probability":-3.59}]}
