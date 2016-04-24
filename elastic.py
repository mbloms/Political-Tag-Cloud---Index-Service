import sys
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from datetime import datetime
import json

class ElasticImporter:
	def __init__(self,path):
		self.es = Elasticsearch()
		self.path = path
		self.index = "tweets"
		self.doc_type = "tweet"
		self.bulk = 100000
		self.importTweets()

	"""Imports all the tweets in the specified file. Usign an
	infinte loop so that we can bulk 25k tweets at the time  useful as we do
	not need to store the whole file as a list, thus not keep eating RAM."""
	def importTweets(self):
		importActions = []
		counter = 0
		acc = 0

		with open(self.path, "r") as file:
			while True:
				line = file.readline()
				if line == "":
					helpers.bulk(self.es, importActions) #bulk import the tweets
					break
				doc = json.loads(line)
				date = doc["date"]
				#Reformats the date to an appropriate format for elasticsearch.
				doc["date"] = datetime.strptime(date,
				"%a %b %d %H:%M:%S %z %Y").isoformat()
				action = {
					'_op_type': 'create',
					"_index": self.index,
					"_type": self.doc_type,
					"_source": doc
					}
				importActions.append(action)
				action = None
				counter +=1
				if counter == self.bulk:
					acc +=self.bulk
					print("I have now processed:" + str(len(importActions)) + " more total:" + str(acc))
					helpers.bulk(self.es, importActions) #bulk import the tweets
					counter = 0 #reset counter
					importActions = [] # reset list
	def checkImport(self):
		self.es.indices.refresh(index=self.index)
		res = self.es.search(index=self.index, body={"query": {"match_all": {}}})
		print("Got %d Hits:" % res['hits']['total'])
		for hit in res['hits']['hits']:
			print("%(user_id)s %(tweet_id)s: %(text)s" % hit["_source"])

def main(path):
	print("Will import " +path  + " into elasticsearch")
	importer = ElasticImporter(path)
	importer.checkImport()

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print("Supplie exactly one argument for the filepath to the datafile.")
	else:
		main(str(sys.argv[1]))
