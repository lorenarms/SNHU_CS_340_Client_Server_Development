
import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://larryarms95:PASSWORD@cluster0.cyqsq.mongodb.net/?retryWrites=true&w=majority")

db = cluster["db"]
collection = db["col"]

		
#delete everything
results = collection.delete_many({})		

post0 = {"_id": 0, "name": "Lawrence", "Age": 38}
post1 = {"_id": 1, "name": "Angelina", "Age": 44}
post2 = {"_id": 2, "name": "Trinity", "Age": 19}
post4 = {"_id": 4, "name": "Ranger", "Age": 5}
		
		

collection.insert_one(post0)


collection.insert_many([post1, post2, post4])

collection.insert_one({"_id": 3, "name": "Sofia", "Age": 17})

#find query
results = collection.find({"name": "Sofia"})
print(results)

for result in results:
	print(result["name"])

results = collection.find_one({"_id": 2})
print(results)

results = collection.find({})
for x in results:
	print(x)


#deleting
results = collection.delete_one({"_id": 0})
results = collection.delete_many({})	


collection.insert_many([post0, post1, {"_id": 3, "name": "Sofia", "Age": 17}, post2] )


#update
collection.update_one({"_id": 3}, {"$set":{"name": "Sofia Day"}})
results = collection.find_one({"_id": 3})
print(results["name"])



#collection.update_one(results["name"], { "$replaceWith": [post4] } )



#delete that one
results=collection.delete_one({"_id": 3})

#update with new field
collection.update_many(
	{},
	{ "$set": {"occupation": "job"} },
	
)

#count documents
count = collection.count_documents({})
print("Total Docs:", count)

results = collection.find_one()
print(results)
