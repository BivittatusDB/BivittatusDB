import BivittatusDB as bdb

#load existing database
db=bdb.database("test").use()

#pull table from database to use
tb1=db("Table1")

print(tb1)