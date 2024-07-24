#make sure to run inside the same directory as BivittatusDB, not the example directory.
import BivittatusDB as bdb

#drop pre-existing databases (for best practice and to prevent errors)
try: bdb.drop("test")
except: pass

#initialize the database
test_db=bdb.database("test").init()

#create a new table 
tb1=test_db.New_table("table1", 
                       ("id", "name"), 
                       (int(), str()), 
                       "id")

#print metadata table (no added rows needed)
print(bdb.metadata(tb1))