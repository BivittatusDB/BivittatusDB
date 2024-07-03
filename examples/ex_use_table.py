import BivittatusDB as bdb

db=bdb.database("new").use()

tb1=db.load_table("Table1")

print(tb1)