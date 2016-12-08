class base_model(object):
	def __init__(self, model_name):
		self.model_name = model_name

	def train(self, dataset):
		pass

	def eval_one(self, sample, method, num_of_output=1):
		pass

	def eval(self, dataset, method):
		pass


