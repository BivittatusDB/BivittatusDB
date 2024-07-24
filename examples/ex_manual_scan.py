#make sure to run inside the same directory as BivittatusDB, not the example directory.
import BivittatusDB as bdb

#drop pre-existing databases (for best practice and to prevent errors)
try: bdb.drop("test")
except: pass

#initialize the database
test_db=bdb.database("test").init()

#create a new table 
tb2=test_db.New_table("table2", 
                       ("id", "name"), 
                       (int(), str()), 
                       "id")

#turn on autocommit for table2
tb2@bdb.ON # Necissary for the referenced table or the refrencer reads wrong data

tb1=test_db.New_table("table1", 
                       ("id", "name"), 
                       (int(), str()), 
                       "id",
                       "table2")

tb2+(3, "Cindy")
tb1+(3, None)

#manually add to data that affects the foreign key
tb1.data.append((1, "Python"))
bdb.scan(tb1) #raises error
