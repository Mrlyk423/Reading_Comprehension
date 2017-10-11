#-*- coding: UTF-8 -*-
class models:
	# data_list 格式：一个列表，每个元素为(D,Q,A)的三元组，如[{"D":"1","Q":"2","A":"3"},...]
	def __init__(self):
		pass
	def train(self, data_list):
		raise NotImplementedError
	def predict(self, data_list):
		raise NotImplementedError
	def save(self,modelname):
		raise NotImplementedError
	def load(self,modelname):
		raise NotImplementedError
	# settings	格式：一个dict
	def setting(self, settings):
		raise NotImplementedError
