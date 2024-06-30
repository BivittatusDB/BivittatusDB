import BivittatusDB as bdb

db=bdb.database("test").use()

tb1=db.load_table("table1")

print(tb1)