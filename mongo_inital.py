import pymongo
import time
Client = pymongo.MongoClient("mongodb://localhost:27017/")
Client.drop_database('BPSS')
DB = Client["BPSS"]
template = {
	'title': 'Template',
	'numOfSentence': 2,
	'pdfHash': 'AHash',
	'allList': ['A', 'B'],
	'combHash:': 'ACombHash',
	'timestamp': time.time(),
	'summary': 0.0,
	'top3List': ['-','-','-']
	}
collection = DB['paper']
res = collection.insert(template)
print(res)