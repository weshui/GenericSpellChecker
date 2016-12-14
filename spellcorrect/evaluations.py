# this class defines a series of interface for evaluation purpose
from numpy import std

class base_evaluator(object):
	def __init__(self, name, model, dataset):
		self.evaluater = name
		self.data = dataset
		self.model = model
		self.ans = []

	def __str__(self):
		return self.evaluater

	def __collect__(self):
		pass

	def mean(self):
		if not self.ans:
			self.__collect__()
		return sum(self.ans)/len(self.ans)

	def std(self):
		if not self.ans:
			self.__collect__()
		return std(self.ans)

	def collect(self):
		if not self.ans:
			self.__collect__()
		return self.ans

	def eval(self):
		for sample in self.data:
			self.eval_one(sample)

	def eval_one(self, sample):
		pass


# expected precision
class precision_eval(base_evaluator):
	def __init__(self, model, dataset):
		super(precision_eval, self).__init__('precision', model, dataset)

	def eval_one(self, sample):
		sample = (wrong_word, right_words)
		temp_ans = set(right_words)
		lis_of_words = self.model.eval_one(wrong_word)
		assert type(lis_of_words) == list
		num_corrects = float(len(set(lis_of_words) & temp_ans))
		self.ans.append(num_corrects / len(lis_of_words))

# expected recall
class recall_eval(base_evaluator):
	def __init__(self, model, dataset):
		super(recall_eval, self).__init__('recall', model, dataset)

	def eval_one(self, sample):
		sample = (wrong_word, right_words)
		temp_ans = set(right_words)
		lis_of_words = self.model.eval_one(wrong_word)
		assert type(lis_of_words) == list
		num_corrects = float(len(set(lis_of_words) & temp_ans))
		self.ans.append(num_corrects / len(temp_ans))

# f1 based on expected recall and precision
class f1_eval(base_evaluator):
	def __init__(self, model, dataset):
		super(recall_eval, self).__init__('f1', model, dataset)
		self.precision = precision_eval(model, dataset)
		self.recall = recall_eval(model, dataset)
		self.ans = None

	def __collect__(self):
		p_lis = self.precision.collect()
		r_lis = self.recall.collect()
		self.ans = [(2 * x * y)/(x+y) for (x,y) in zip(p_lis, r_lis)]

	def eval_one(self, sample):
		self.precision.eval_one(sample)
		self.recall.eval_one(sample)


SUPPORTED_METHOD = {'precision' : precision_eval, 'recall' : recall_eval, 'f1' : f1_eval}

from models import base_model
from datasets import base_dataset
class simple_eval(object):

	def __init__(self, method, model, dataset):
		assert isinstance(model, base_model)
		assert isinstance(dataset, base_dataset)
		assert method in SUPPORTED_METHOD.keys()
		self.evaluator = SUPPORTED_METHOD[method](model, dataset)
		self.evaluator.eval()

	def mean(self):
		return self.evaluator.mean()

	def collect(self):
		return self.evaluator.collect()

	def std(self):
		return self.evaluator.std()









