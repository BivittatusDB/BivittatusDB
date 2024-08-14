#make sure to run inside the same directory as BivittatusDB, not the example directory.
import BivittatusDB as bdb

#This module needs test
def print_metadata():
    #initialize the database
    test_db=bdb.database("test").init()

    #create a new table 
    tb1=test_db.New_table("table1", 
                        ("id", "name"), 
                        (int(), str()), 
                        "id")

    #print metadata table (no added rows needed)
    print(bdb.metadata(tb1))