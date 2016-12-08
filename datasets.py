SUPPORTED_MODEL = ['unigram', 'bigram']

class NotSupportedError(Exception):
	def __init__(self, name):
		self.name = name
	def __str__(self):
		return "%s is currently not supported"


# defines what should go into each dataset
class base_dataset(object):
	def __init__(self, dataset_name):
		self.dataset_name = dataset_namename

	def load(self, file):
		pass

	def next(self):
		pass

	# a generator
	def next_gen(self):
		pass

# a supervised dataset of ngrams
# return a generator 
class supervised_dataset(object):
	def __init__(self, model):
		if model not in SUPPORTED_MODEL:
			raise NotSupportedError(model)
			return None

		self.data = None
		elif model == 'unigram':
			self.datamodel = 'unigram'

	def __gen__(self, datafile, delimeter, user_defined=None):
		for line in open(datafile, 'r'):
			if not user_defined:
				lis = line.split(delimeter)
				if self.datamodel == 'unigram':
					assert (len(lis) == 2),"line %s does not fit format data%slabel" % (line, delimeter)
			else:
				lis = user_defined(line)
			yield lis

	def load(self, datafile, delimeter=',', line_prop=None):
		self.data = __gen__(datafile, delimeter, user_defined=line_prop)

	def next(self):
		assert (self.data != None),"data is not initalized"
		return self.data.next()

