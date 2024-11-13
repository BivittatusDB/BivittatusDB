#make sure to run inside the same directory as BivittatusDB, not the example directory.
import BivittatusDB as bdb

#drop pre-existing databases (for best practice and to prevent errors)
try: bdb.drop("test")
except bdb.BDBException.DeletionError: pass

#initialize the database
test_db=bdb.Database("test").init()

#create a new table
tb1=test_db.new_table("table1",  #named table1
                       ("id", "name"), #with columns "id" and "name"
                       (int, str), #that hold integers and string (respectivley)
                       "id") #and the primary key is the id column

#print database (empty)
print(tb1)