#make sure to run inside the same directory as BivittatusDB, not the example directory.
import BivittatusDB as bdb

#drop pre-existing databases (for best practice and to prevent errors)
try: bdb.drop("test")
except: pass

#initialize the database
test_db=bdb.database("test").init()

#create a new table 
tb1=test_db.New_table("table1", #name "table1"
                       ("id", "name"), #columns are called "id" and "name"
                       (int(), str()), #id holds int, and name holds str
                       "id") #id will be the primary key

#add rows to the table
tb1+(1, "Alice") 
tb1+(2, "Bob")
tb1+(3, "Cindy")