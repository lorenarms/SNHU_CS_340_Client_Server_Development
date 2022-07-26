import CRUD
from CRUD import CRUD


c = CRUD()

c.deleteAll()
c.builddb()


#CREATE
d = {"_id": 5, "name":"Smoke", "Age": 15}
c.create(d)
c.create(d)


#READ
c.read(d)
c.read(d)
c.read(None)
c.read({"Age":15})
c.read({"name":"Lawrence"})
c.read({"name":"lawrence"})
c.read({"name":"Larry"})
c.read({"name":"Lawrence"})


#UPDATE
e = {"name":"Puck"}
c.update(d, e)
c.read(d)
c.update({"name":"Lawrence"},{"name":"Larry"})
c.read({"name":"Larry"})


#DELETE
c.delete({"name":"Puck"})
c.read({"name":"Puck"})
c.delete({"name":"Puck"})





