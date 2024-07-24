#make sure to run inside the same directory as BivittatusDB, not the example directory.
import BivittatusDB as bdb

try: bdb.drop("test")
except: pass

test_db=bdb.database("test").init()

tb1=test_db.New_table("table1", 
                       ("id", "name"), 
                       (int(), str()), 
                       "id")

print(tb1)