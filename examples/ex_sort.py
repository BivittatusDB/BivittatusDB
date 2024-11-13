#make sure to run inside the same directory as BivittatusDB, not the example directory.
import BivittatusDB as bdb

#drop pre-existing databases (for best practice and to prevent errors)
try: bdb.drop("test")
except bdb.BDBException.DeletionError: pass

#initialize the database
test_db=bdb.Database("test").init()

#create a new table
tb1=test_db.new_table("table1", 
                       ("id", "name"), 
                       (int, str), 
                       "id")

#add rows to the table
tb1+(1, "Alice")
tb1+(3, "Cindy")
tb1+(2, "Bob")

print(tb1)
#sort data by column "id"
print(tb1*"id")