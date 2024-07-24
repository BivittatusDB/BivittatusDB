import BivittatusDB as bdb

#load existing database
db=bdb.database("new").use()

#pull table from database to use
tb1=db.load_table("Table1")

print(tb1)