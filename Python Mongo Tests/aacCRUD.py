import pymongo
from pymongo import MongoClient

import json

class CRUD(object):

	def __init__(self):
		self.cluster = MongoClient('mongodb://localhost:27017')
		self.db = self.cluster["AAC"]
		self.collection = self.db["animals"]
		print("SUCCESS: Accessed database")

	#CREATE
	def create(self, data):
		s = json.dumps(data)	
		if data is None or data == {}:
			print("ERROR - No data was passed in")
		else:
			results = self.collection.find_one(data)
			if results is None:
				self.collection.insert_one(data)
				print("SUCCESS - " + s + " was successfully added.")
			else:
				print("ERROR - Data " + results["name"] + " already in database.")
		
	#READ
	def read(self, data):
		s = json.dumps(data)
		if data is None or data == {}:
			print("ERROR - No data was passed in")
		else:
			results = self.collection.find_one(data)
			if results is None:
				print("ERROR - " + s + " was not found")
			else:
				results = self.collection.find(data)
				count = 0
				for item in results:
					print("SUCCESS - " + s + " was found")
					count+=1
				print(str(count) + " total document(s) containing " + s + " were found")
		
		
	#UPDATE
	def update(self, data, replace):
		d = json.dumps(data)
		r = json.dumps(replace)
		if data is None or data == {}:
			print("ERROR - No data was passed in")
		else:
			results = self.collection.find_one(data)
			if results is None:
				print("ERROR - " + s + " was not found")
			else:
				results = self.collection.find(data)
				for item in results:
					self.collection.update_one(data, {"$set": replace})
					print("SUCCESS - updated " + d + " to " + r)

	
	

	#DELETE
	def delete(self, data):
		d = json.dumps(data)
		if data is None or data == {}:
			print("ERROR - No data was passed in")
		else:
			results = self.collection.find_one(data)
			if results is None:
				print("ERROR - " + d + " was not found")
			else:
				self.collection.delete_one(data)
				s = json.dumps(data)
				print("SUCCESS - " + s + " deleted")


	