# this class contains a list of predefined models and a base model


# based model, defines what should be implemented for any particular model
class base_model(object):
	def __init__(self, model_name):
		self.model_name = model_name

	def train(self, dataset):
		pass # enter how do you want to train your model below

	def eval_one(self, sample):
		pass # enter how your model will evaluate on one input

# this class is for testing purpose
class plain_model(base_model):
	def __init__(self, model_name):
		super(plain_model, self).__init__(model_name)

	# identity word
	def eval_one(self, sample):
		return [sample]
		