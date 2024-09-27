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
                       (int, str), 
                       "id")

#add rows to table1
tb1+(1, "Alice")
tb1+(2, "Bob")
tb1+(3, "Cindy")

print(tb1)

#remove all rows that hold the value "Bob" in column "name"
tb1["name"]-"Bob"

print(tb1)