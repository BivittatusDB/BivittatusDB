import metaclass
try: 
    from statistics import *
    import shutil
    import os
    import platform
    import time
except:
    raise metaclass.BDBException.ImportError(f"Could not import needed files in {__file__}")

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

def drop(database:str):
    '''drops a database and allows for reinitialization'''
    try:
        shutil.rmtree(database)
    except:
        raise metaclass.BDBException.DeletionError("Could not drop database {database}")

#True and False commands for auto commit
ON=True
OFF=False
ALL=None
PRIMARY=None
VERBOSE=ON

class infomessage():
    def __init__(self, message: str, **print_kwargs) -> None:
        if VERBOSE:
            print(message, **print_kwargs)

#aggregate functions for stage 3
def ensure_column(table):
    try:
        table.column
    except:
        raise metaclass.BDBException.ColumunError("Must select column to use aggregate function")

def COUNT(table):
    try:
        return len(table)
    except:
        raise metaclass.BDBException.AggregateError("Unable to perform aggregate function")

def SUM(table):
    try:
        ensure_column(table)
        return sum(table.column)
    except:
        raise metaclass.BDBException.AggregateError("Unable to perform aggregate function")

def AVG(table):
    try:
        ensure_column(table)
        return SUM(table)/COUNT(table)
    except:
        raise metaclass.BDBException.AggregateError("Unable to perform aggregate function")

def MIN(table):
    try:
        ensure_column(table)
        return min(table.column)
    except:
        raise metaclass.BDBException.AggregateError("Unable to perform aggregate function")

def MAX(table):
    try:
        ensure_column(table)
        return max(table.column)
    except:
        raise metaclass.BDBException.AggregateError("Unable to perform aggregate function")

def STDEV(table):
    try:
        ensure_column(table)
        return stdev(table.column)
    except:
        raise metaclass.BDBException.AggregateError("Unable to perform aggregate function")

def STDEVP(table):
    try:
        ensure_column(table)
        return pstdev(table.column)
    except:
        raise metaclass.BDBException.AggregateError("Unable to perform aggregate function")

def MODE(table):
    try:
        ensure_column(table)
        return mode(table.column)
    except:
        raise metaclass.BDBException.AggregateError("Unable to perform aggregate function")

def MEDIAN(table):
    try:
        ensure_column(table)
        return median(table.column)
    except:
        raise metaclass.BDBException.AggregateError("Unable to perform aggregate function")

def FIRST(table):
    try:
        ensure_column(table)
        return table.column[0]
    except:
        raise metaclass.BDBException.AggregateError("Unable to perform aggregate function")

def LAST(table):
    try:
        ensure_column(table)
        return table.column[-1]
    except:
        raise metaclass.BDBException.AggregateError("Unable to perform aggregate function")

#A screan cleaner with delay
def pause_and_clean(duration):
    time.sleep(duration)
    
    # Check the operating system using platform.system()
    system_name = platform.system()
    
    if system_name == 'Windows':
        os.system('cls')
    elif system_name in ['Linux', 'Darwin']:  # Darwin' is for macOS
        os.system('clear')
    else:
        raise NotImplementedError(f"The operating system '{system_name}' is not supported for clearing the screen.")

# Example
#pause_and_clean(2)  
# Pause for 2 seconds and then wipe the screen.