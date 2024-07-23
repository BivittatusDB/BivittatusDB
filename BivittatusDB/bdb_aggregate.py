from statistics import *

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
def ensure_column(table):
    try:
        table.column
    except:
        raise AttributeError("Must select column to use aggregate function")

def COUNT(table):
    return len(table)
def SUM(table):
    ensure_column(table)
    return sum(table.column)
def AVG(table):
    ensure_column(table)
    return SUM(table)/COUNT(table)
def MIN(table):
    ensure_column(table)
    return min(table.column)
def MAX(table):
    ensure_column(table)
    return max(table.column)
def STDEV(table):
    ensure_column(table)
    return stdev(table.column)
def STDEVP(table):
    ensure_column(table)
    return pstdev(table.column)
def MODE(table):
    ensure_column(table)
    return mode(table.column)
def MEDIAN(table):
    ensure_column(table)
    return median(table.column)
def FIRST(table):
    ensure_column(table)
    return table.column[0]
def LAST(table):
    ensure_column(table)
    return table.column[-1]