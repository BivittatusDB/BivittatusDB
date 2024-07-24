import BivittatusDB as bdb

try: bdb.drop("test")
except: pass

test_db=bdb.database("test").init()

tb1=test_db.New_table("table1", ("id", "name"), (int(), str()), "id")
tb2=test_db.New_table("table2", ("id", "language"), (int(), str()), "id")

tb1+(1, "Alice")
tb1+(2, "Bob")
tb1+(3, "Cindy")

tb2+(1, "Python")
tb2+(2, "Java")
tb2+(4, "C++")

print(tb1)
print(tb2)
print(tb1<<tb2) #left join
print(tb1>>tb2) #right join
print(tb1^tb2)  #full join