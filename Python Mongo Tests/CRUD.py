import pymongo
from pymongo import MongoClient

class CRUD(object):

	def __init__(self):
		self.cluster = MongoClient("mongodb+srv://larryarms95:RaqtcUEphXtg5rJH@cluster0.cyqsq.mongodb.net/?retryWrites=true&w=majority")
		self.db = self.cluster["db"]
		self.collection = self.db["col"]

		self.collection.delete_many({});

		print("SUCCESS - accessed database")

	def builddb(self):

		post0 = {"_id": 0, "name": "Lawrence", "Age": 38}
		post1 = {"_id": 1, "name": "Angelina", "Age": 44}
		post2 = {"_id": 2, "name": "Trinity", "Age": 19}
		post4 = {"_id": 4, "name": "Ranger", "Age": 5}

		self.collection.insert_one({"_id": 3, "name": "Sofia", "Age": 17})

		self.collection.insert_many([post0, post1, post2, post4])

		print("SUCCESS - built a new database")


	#CREATE
	def create(self, data):
			if data is None or data == {}:
				print("ERROR - No data was passed in")
			else:
				results = self.collection.find_one(data)
				if results is None:
					self.collection.insert_one(data)
					print("SUCCESS - " + data["name"] + " was successfully added.")
				else:
					print("ERROR - Data " + results["name"] + " already in database.")
		

	#READ
	def read(self, data):
		if data is None or data == {}:
			print("ERROR - No data was passed in")
		else:
			results = self.collection.find_one(data)
			if results is None:
				print("ERROR - " + data["name"] + " was not found")
			else:
				results = self.collection.find(data)
				for item in results:
					print("SUCCESS - found " + item["name"])

		
		
	#UPDATE
	def update(self, data, new):
		if data is None or data == {}:
			print("ERROR - No data was passed in")
		else:
			results = self.collection.find_one(data)
			if results is None:
				print("ERROR - That data was not found")
			else:
				results = self.collection.find(data)
				for item in results:
					self.collection.update_one(data, {"$set": new})
					print("SUCCESS - updated " + new["name"])

	
	

	#DELETE
	def delete(self, data):
		if data is None or data == {}:
			print("ERROR - No data was passed in")
		else:
			results = self.collection.find_one(data)
			if results is None:
				print("ERROR - That data was not found")
			else:
				self.collection.delete_one(data)
				print("SUCCESS - " +data["name"] + " deleted")


	