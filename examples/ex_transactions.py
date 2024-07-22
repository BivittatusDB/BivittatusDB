#make sure to run inside the same directory as BivittatusDB, not the example directory.
import BivittatusDB as bdb

test_db=bdb.database("test").init()

tb1=test_db.New_table("table1", 
                       ("id", "name"), 
                       (int(), str()), 
                       "id")

tb1+(1, "Alice")
tb1+(2, "Bob")
print(type(bdb.table))

bdb.SAVEPOINT@tb1

tb1+(3, "Cindy")
print(tb1)

bdb.ROLLBACK@tb1

print(tb1)

bdb.COMMIT@tb1