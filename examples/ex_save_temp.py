import BivittatusDB as bdb

#drop pre-existing databases (for best practice and to prevent errors)
try: bdb.drop("test")
except: pass

#initialize the database
test_db=bdb.database("test").init()

#create tables
tb1=test_db.New_table("table1", ("id", "name"), (int, str), "id")
tb2=test_db.New_table("table2", ("id", "language"), (int, str), "id")

#add rows to the tables
tb1+(1, "Alice")
tb1+(2, "Bob")
tb1+(3, "Cindy")

tb2+(1, "Python")
tb2+(2, "Java")
tb2+(4, "C++")

print(tb1)
print(tb2)
tb3=tb1^tb2 #do a full join of the tables
print(tb3)

#save a new table that hold the output of the join 
bdb.save(tb3, "table3", (int(), str(), str()))

#load the table into the code
tb4=test_db("table3")
print(tb4)