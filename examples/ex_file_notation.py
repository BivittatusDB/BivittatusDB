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

#add data to the table
tb1.write((1, "Alice"))
tb1.write((2, "Bob"))

#the write function is compatible with using the file argument of print
print((3,"Cindy"), file=tb1)

#Read data from a table
#read all data (prints raw)
print(tb1.read())

#Read one line at a time
print(tb1.readline())
print(tb1.readline())
print(tb1.readline())

#Read a specific line
print(tb1.readline(1))

#change position
#Postion options
#   0 = File beginning
#   1 = Current Position
#   2 = End of File
tb1.seek(0,0) #0 lines from the begging of the file

#get current position
print(tb1.tell())

#Read several lines starting at current position
print(tb1.readlines(2))

#write to disk
tb1.flush()