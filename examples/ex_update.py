#make sure to run inside the same directory as BivittatusDB, not the example directory.
import BivittatusDB as bdb

#drop pre-existing databases (for best practice and to prevent errors)
try: bdb.drop("test")
except bdb.BDBException.DeletionError: pass

#initialize the database
test_db=bdb.Database("test").init()

#make a new table
tb1=test_db.new_table("table1", 
                       ("id", "name"), 
                       (int, str), 
                       "id",
                       None)

#add data to the table
tb1+(1, "Alice")
tb1+(2, "Bob")
tb1+(3, "Cindy")

print(tb1)

#example updates
#Set the name "Cindy" to "Chloe"
tb1[1] = (tb1["name"]=="Cindy", "Chloe")

print(tb1)

#Set all names to "new_name"
tb1["name"] = (bdb.ALL, "new_name")

print(tb1)