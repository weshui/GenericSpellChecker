# this file defines a list of exisiting dataset

SUPPORTED_MODEL = ['unigram', 'bigram']

class NotSupportedError(Exception):
	def __init__(self, name):
		self.name = name
	def __str__(self):
		return "%s is currently not supported"

# defines what should go into each dataset
class base_dataset(object):
	def __init__(self, datasetname):
		self.datasetname = datasetname
		self.data = None

	def __gen__(self, datafile, delimeter, user_defined=None):
		for line in open(datafile, 'r'):
			lis = line.split(delimeter) if not user_defined else user_defined(line)
			yield lis

	def load(self, file):
		pass

	def next(self):
		try:
			return self.data.next()
		except AttributeError: # data is not initalized
			print 'please initalize the dataset first'

# return a dictionary of words
class dictionary(base_dataset):
	def __init__(self, datasetname):
		super(dictionary, self).__init__(dataset_name)

	def load(self, datafile, delimeter=None, user_defined=None):
		self.data = self.__gen__(datafile, delimeter, user_defined)

	# flatten
	def next(self):
		try:
			for lis in self.data.next():
				for word in lis:
					yield word
		except AttributeError: # data is not initalized
			print 'please initalize the dataset first'


# a supervised dataset of ngrams
# return a generator 
class supervised_dataset(base_dataset):
	def __init__(self, datasetname, model):
		super(supervised_dataset, self).__init__(dataset_name)
		if model not in SUPPORTED_MODEL:
			raise NotSupportedError(model)
			return None

		self.data = None
		elif model == 'unigram':
			self.datamodel = 'unigram'

	# def split_cv(self, copies):
		
	def load(self, datafile, delimeter=',', user_defined=None):
		self.data = self.__gen__(datafile, delimeter, user_defined=line_prop)
		
