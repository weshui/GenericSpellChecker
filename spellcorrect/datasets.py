# this file defines a list of exisiting dataset
import types
import inspect

# defines the supported language model
SUPPORTED_MODEL = ['unigram', 'bigram']

# defines a list of errors thrown by this modules
class NotSupportedError(Exception):
	def __init__(self, name):
		self.name = name
	def __str__(self):
		return "%s is currently not supported"

# defines what should go into each dataset
class base_dataset(object):

	# constructor of base dataset
	def __init__(self, datasetname):
		self.datasetname = datasetname
		self.data = None

	# return a genertor for processing data
	def __gen__(self, datafile, delimeter=' ', line_prop=None, output_prop=None):
		for line in open(datafile, 'r'):
			line = line.strip()
			lis = line.split(delimeter) if not line_prop else line_prop(line)
			if output_prop:
				if inspect.isgeneratorfunction(output_prop):
					for output in output_prop(lis):
						yield output
				else:
					yield output_prop(lis)
			else:
				yield lis

	# return nothing, but will load the data and initalize the self.data part
	def load(self, file):
		pass

	# in case user want to use it as a list, base dataset also defines the next()
	def next(self):
		try:
			return self.data.next()
		except AttributeError: # data is not initalized
			print 'please initalize the dataset first'

# return a dictionary of words
class dictionary(base_dataset):

	# constructor for dictionary dataset
	def __init__(self, datasetname):
		super(dictionary, self).__init__(datasetname)

	# defines to load a dictionary
	def load(self, datafile, delimeter=None, line_prop=None, output_prop=None):
		self.data = self.__gen__(datafile, delimeter, line_prop=line_prop, output_prop=output_prop)

	# flatten the generator
	def next(self):
		try:
			for lis in self.data.next():
				for word in lis:
					yield word
		except AttributeError: # data is not initalized
			print 'please initalize the dataset first'


# a supervised dataset of ngrams
class supervised_dataset(base_dataset):

	# constructor
	def __init__(self, datasetname, model):
		super(supervised_dataset, self).__init__(datasetname)
		if model not in SUPPORTED_MODEL:
			raise NotSupportedError(model)
			return None
		elif model == 'unigram':
			self.datamodel = 'unigram'
		elif model == 'bigram':
			self.datamodel = 'bigram'
		
	# load data into this dataset
	def load(self, datafile, delimeter=',', line_prop=None, output_prop=None):
		self.data = self.__gen__(datafile, delimeter, line_prop=line_prop, output_prop=output_prop)
		
# load a predefined spellerror dataset
def load_spellerror():
	ds = supervised_dataset('spell-error', 'unigram')
	def line_seperated(line):
		cur_line = map(lambda x: x.strip(), line.split(':'))
		cur_line[-1] = cur_line[-1].split(', ')
		return cur_line
	def output_gen(lis):
		[correct_word, wrong_word_lis] = lis
		for wrong_word in wrong_word_lis:
			yield [correct_word, wrong_word]
	ds.load('../corpus/spell-errors.txt', line_prop=line_seperated, output_prop=output_gen)
	return ds

# load a predefeind small dictionary dataset
def load_small_dictionary():
	ds = dictionary('small-1w')
	ds.load('../corpus/count_1w.txt', delimeter='\t')
	return ds


