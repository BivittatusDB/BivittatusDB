#make sure to run inside the same directory as BivittatusDB, not the example directory.
import BivittatusDB as bdb

try: bdb.drop("test")
except: pass

test_db=bdb.database("test").init()

tb1=test_db.New_table("table1", 
                       ("id", "name"), 
                       (int(), str()), 
                       "id",
                       None)

tb1+(1, "Alice")
tb1+(2, "Bob")
tb1+(3, "Cindy")

print(tb1)

#Set the name "Cindy" to "Chloe"
tb1[1] = ("Chloe", tb1["name"]=="Cindy")

print(tb1)

#Set all names to "new_name"
tb1["name"] = ("new_name", bdb.ALL)

print(tb1)