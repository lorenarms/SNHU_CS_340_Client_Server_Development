import aacCRUD
from aacCRUD import CRUD


a = CRUD()


a.read({"name":"Frank"})
a.read({"name":"Kitty"})
a.create({"name":"Sofia Jade"})

a.update({"name":"Sofia Jade"},{"name":"Trinity Sofia"})

a.delete({"name":"Sofia Jade"})
a.delete({"name":"Trinity Sofia"})