'''This will be used for aggregate functions. Will be imported with * to ./BivittatusDB.py'''
#extra functions 
def save(table, name=None, types=None):
    '''save the specified table. Must be called to commit changes.'''
    getattr(table, "__save__")(name, types)
    
def metadata(table):
    '''returns the metadata of specified table as a table. Metadata table does not have metadata.'''
    return getattr(table, "__load_metadata__")()

def scan(table):
    '''scans a table for errors if updated manually'''
    getattr(table, "__scan__")()
    return True

#True and False commands for auto commit
ON=True
OFF=False
ALL=None

#aggregate functions for stage 3
def COUNT(): pass
def SUM(): pass
def AVG(): pass
def MIN(): pass
def MAX(): pass
def STDEV(): pass
def STDEVP(): pass
def MEDIAN(): pass
def MODE(): pass
def FIRST(): pass
def LAST(): pass
