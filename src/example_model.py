from models import models


class example_model(models):
	def __init__(self):
		models.__init__(self)
	def train(self, data_list):
		print "train",data_list[:10]
	def predict(self, data):
		print "predict",data
	def setting(self, settings):
		raise "settings", settings
	def save(self,modelname):
		print "save"
	def load(self,modelname):
		print 'load'