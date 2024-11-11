#make sure to run inside the same directory as BivittatusDB, not the example directory.
import BivittatusDB as bdb

#drop pre-existing databases (for best practice and to prevent errors)
try: bdb.drop("test")
except: pass

#initialize the database
test_db=bdb.Database("test").init()

#create a new table 
tb1=test_db.new_table("table1", 
                       ("id", "name", "age"), 
                       (int, str, int), 
                       "id")
#add rows to the table
tb1+(1, "Alice", 24)
tb1+(2, "Bob", 36)
tb1+(3, "Cindy", 19)

#aggregate functions defined so far
print(tb1)
print("Length:",bdb.COUNT(tb1)) 
print("SUM:", bdb.SUM(tb1["age"])) 
print("AVG:",bdb.AVG(tb1["age"]))
print("MIN:",bdb.MIN(tb1["age"]))
print("MAX:",bdb.MAX(tb1["age"]))
print("STDEV:",bdb.STDEV(tb1["age"]))
print("STDEVP:",bdb.STDEVP(tb1["age"]))
print("MODE:",bdb.MODE(tb1["age"]))
print("MEDIAN:",bdb.MEDIAN(tb1["age"]))
print("FIRST:", bdb.FIRST(tb1["age"]))
print("LAST:",bdb.LAST(tb1["age"]))