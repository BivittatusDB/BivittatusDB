#make sure to run inside the same directory as BivittatusDB, not the example directory.
import BivittatusDB as bdb

test_db=bdb.database("test").init()

tb1=test_db.make_table("table1", 
                       ("id", "name", "age"), 
                       (int(), str(), int()), 
                       "id")

tb1+(1, "Alice", 24)
tb1+(2, "Bob", 36)
tb1+(3, "Cindy", 19)

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