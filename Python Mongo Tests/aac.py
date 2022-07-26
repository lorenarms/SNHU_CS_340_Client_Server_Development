import aacCRUD
from aacCRUD import CRUD

#LOCAL Mongodb (for testing purposes)
a = CRUD('mongodb://localhost:27017')

b = CRUD("mongodb+srv://aacuser:PASSWORD@cluster0.cyqsq.mongodb.net/?retryWrites=true&w=majority")

#Insert all data into database (data already in)
#b.mongoimport("C:\\Users\\Lawrence\\Downloads\\aacdb.csv")

print("LOCAL")
a.read({"name":"Kitty"})

print("CLOUD")
b.read({"name":"Frank"})
