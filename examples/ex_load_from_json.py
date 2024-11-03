#make sure to run inside the same directory as BivittatusDB, not the example directory.
import BivittatusDB as bdb

db = bdb.database("test")

db.init_from_json("test.json")