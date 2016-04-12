import sys
from elasticsearch import Elasticsearch
from datetime import datetime
import json

class ElasticImporter:
	def __init__(self,path):
		self.es = Elasticsearch()
		self.path = path

	def importTweets(self):

		with open("test100k.json", "r") as data_file:
			for line in data_file:
				doc = json.loads(line)
				user_id = doc["user_id"]
				res = es.index(index="test-index", doc_type='tweet', body=doc)
				print(res['created'])

		es.indices.refresh(index="test-index")

		res = es.search(index="test-index", body={"query": {"match_all": {}}})
		print("Got %d Hits:" % res['hits']['total'])
		for hit in res['hits']['hits']:
		    print("%(user_id)s %(tweet_id)s: %(text)s" % hit["_source"])
def main(args):
	print(args)

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print("Supplie exactly one argument for the filepath to the datafile.")
	else:
		main(str(sys.argv[1]))
