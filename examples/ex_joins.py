import BivittatusDB as bdb

#drop pre-existing databases (for best practice and to prevent errors)
try: bdb.drop("test")
except bdb.BDBException.DeletionError: pass

#initialize the database
test_db=bdb.Database("test").init()

#create new tables
tb1=test_db.new_table("table1", 
                      ("id", "name"), 
                      (int, str), 
                      "id")

tb2=test_db.new_table("table2", 
                      ("id", "language"), 
                      (int, str), 
                      "id")

#add rows to table1
tb1+(1, "Alice")
tb1+(2, "Bob")
tb1+(3, "Cindy")

#add rows to table2
tb2+(1, "Python")
tb2+(2, "Java")
tb2+(4, "C++")

print(tb1)
print(tb2)

#join the tables
print(tb1<<tb2) #left join
print(tb1>>tb2) #right join
print(tb1^tb2)  #full join