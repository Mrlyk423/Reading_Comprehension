import os,sys
import example_model
import json


train_filename = "../data/SQuAD-v1.1-train.json"
dev_filename = "../data/SQuAD-v1.1-dev.json"


def load_data(filename):
	res = []
	f = open(filename, "r")
	json_str = "".join(f.readlines())
	data = json.loads(json_str)
	for doc in data["data"]:
		print doc['title']
		for paragraph in doc["paragraphs"]:
			print paragraph['context']
			for qas in paragraph['qas']:
				qas_dict= {"D":paragraph['context'],"A":qas["answers"][0],"Q":qas["question"]}
				res.append(qas_dict)
	return res



if __name__ == "__main__":
	train_data_list = load_data(train_filename)
	dev_data_list = load_data(dev_filename)

	model = example_model.example_model()
	#模型参数设置
	model.setting({})
	#模型训练
	model.train(data_list)

	#模型保存加载
	model.save(modelname)
	model.load(modelname)

	#模型预测，返回一个list，每个元素为对应预测答案

	model.predict(data_list)