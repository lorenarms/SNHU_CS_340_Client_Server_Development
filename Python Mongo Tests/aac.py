#Lawrence Artl III
#CS 340 22EW6
#Project 1 - TESTER - SUBLIME TEXT
#July 28, 2022

import aacCRUD
from aacCRUD import CRUD

import json
from bson.json_util import dumps, loads

#LOCAL Mongodb (for testing purposes)
a = CRUD('mongodb://localhost:27017')

#CLOUD Mongodb (for deployment)
#Access through Atlas via Mongodb.com
b = CRUD("mongodb+srv://aacuser:yh0okRBJkaFVCJnw@cluster0.cyqsq." + 
	"mongodb.net/?retryWrites=true&w=majority")

#Insert all data into cloud database (completed)
#b.mongoimport('C:\\Users\\Lawrence\\Downloads\\aacdb.csv')

print("LOCAL")
#create new document
a.create({"name":"Lorenzo"})
#find created document
a.read({"name":"Lorenzo"})
#update name of document
a.update({"name":"Lorenzo"}, {"name":"Lawrence"})
#find updated document
s = a.read({"name":"Lawrence"})
#find old version of updated document
a.read({"name":"Lorenzo"})


print("ALL DATA")
for doc in s:
	print(doc)
print(s)

#delete document
a.delete({"name":"Lawrence"})
#find deleted document
a.read({"name":"Lawrence"})


print("CLOUD")
#create new document
b.create({"name":"Lorenzo"})
#find created document
b.read({"name":"Lorenzo"})
#update name of document
b.update({"name":"Lorenzo"}, {"name":"Lawrence"})
#find updated document
b.read({"name":"Lawrence"})
#find old version of updated document
b.read({"name":"Lorenzo"})
#delete document
b.delete({"name":"Lawrence"})
#find deleted document
b.read({"name":"Lawrence"})
