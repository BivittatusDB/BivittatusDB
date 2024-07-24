#make sure to run inside the same directory as BivittatusDB, not the example directory.
import BivittatusDB as bdb

try: bdb.drop("test")
except: pass

test_db=bdb.database("test").init()

tb2=test_db.New_table("table2", 
                       ("id", "name"), 
                       (int(), str()), 
                       "id")
tb2@bdb.ON # Necissary for the referenced table or the refrencer reads wrong data

tb1=test_db.New_table("table1", 
                       ("id", "name"), 
                       (int(), str()), 
                       "id",
                       "table2")

tb2+(3, "Cindy")
tb1+(3, None)

#manually add an error that affects the foreign key
tb1.data.append((1, "Python"))
bdb.scan(tb1) #raises error
