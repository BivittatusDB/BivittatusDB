'''This will be used for aggregate functions. Will be imported with * to ./BivittatusDB.py'''
#extra functions 
def save(table):
    '''save the specified table. Must be called to commit changes.'''
    getattr(table, "__save__")()
    
def metadata(table):
    '''returns the metadata of specified table as a table. Metadata table does not have metadata.'''
    return getattr(table, "__load_metadata__")()

#True and False commands for auto commit
ON=True
OFF=False