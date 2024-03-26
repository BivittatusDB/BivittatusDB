#Class for making metadata tables, simplified version of the class in ./py_table.py
#no checks for data types, loading metadata (for obvious reasons), primary keys.
#In short: metadata table with no metametadata

import pydb_io as io, json, datetime
from typing import Union

class table:
    def __init__(self, database, table_name, temp:bool=False, temp_data:list=None) -> None:
        self.database=database
        self.table_name="meta_"+table_name
        self.temp=temp
        if self.temp==False:
            self.__read__()
        else:
            self.data=temp_data
            self.columns=self.data.pop(0)

    def __read__(self):
        '''Read data from a file'''
        reader=io.read(self.database)
        self.data=json.loads(reader.read_table(self.table_name))
        self.columns=self.data.pop(0)

    def __write__(self, new_table):
        '''Write a new table to database. Not used currently'''
        writer=io.write(self.database)
        data=json.dumps([self.columns]+self.data)
        writer.write_table(new_table, data)
    
    def __edit__(self):
        '''Change data in database table. Used in the __save__ method'''
        editor=io.edit(self.database)
        new_data=json.dumps([self.columns]+self.data)
        editor.edit_table(self.table_name, new_data)

    def __save__(self):
        '''Commit changes to database. Call using save function in main file'''
        self.temp=False
        self.__edit__()

    def __repr__(self) -> list:
        '''return raw data. Call with repr(self)'''
        return self.__read__()
    
    def __str__(self) -> str:
        '''return formatted data. Call using print(self)'''
        table=""
        data=self.data
        first_row=self.columns
        col_widths=[max(len(str(item)) for item in col) for col in zip(*(data+[first_row]))]
        table+="+"+"+".join("-"*(width) for width in col_widths)+"+\n"
        table+="|"+"|".join(str(item).ljust(width) for item,width in zip(first_row, col_widths))+"|\n"
        table+="+"+"+".join("-"*(width) for width in col_widths)+"+\n"
        for row in data:
            table+="|"+"|".join(str(item).ljust(width) for item,width in zip(row, col_widths))+"|\n"
        table+="+"+"+".join("-"*(width) for width in col_widths)+"+\n"
        return table

    def __len__(self)->int:
        '''return the number of values in the data'''
        return len(self.data)
    
    def __getitem__(self, key: Union[int, str]):
        '''return a column from the data. Requirement to compare data'''
        self.column=[]
        data=self.data
        colums=self.columns
        if type(key)==type(str()):
            key=colums.index(key)
        for row in data:
            self.column.append(row[key])
        return self
    
    def __setitem__(self, key, value):
        '''change column name. Will probably change later.'''
        columns=self.columns
        columns[key]=value

    def __iter__(self):
        '''start iterations. Call using `for item in self`'''
        self.index=0
        return self
    
    def __next__(self):
        '''increment iterations'''
        data=self.data
        if self.index<len(self):
            value=data[self.index]
            self.index+=1
            return value
        else:
            raise StopIteration
        
    def __contains__(self, item):
        '''checks to see if item is in data. Call using `item in self`'''
        if not self.column:
            raise IndexError("Must index a column to search item")
        if item in self.column:
            del self.column
            return True
        del self.column
        return False
    
    def __matmul__(self, key:int):
        '''sort a the data by specified column (key). call using self@key'''
        self.data=sorted(self.data, key=lambda x: x[key])

    def __add__(self, value:list):
        '''add new row to the table. call using self+value'''
        self.data.append(value)

    def __find_compare__(self, operator:str, value):
        '''used to remove all data not meeting opperator requirments.'''
        if not self.column:
            raise IndexError(f"Must Index Column to use comparison {operator}")
        data=self.column
        rows=[]
        for i in range(len(data)):
            if eval(f"data[i]{operator}value"):
                rows.append(i)
        return rows
    
    def __sub__(self, value):
        '''remove all rows containing value in specified column'''
        rows=self.__find_compare__("==", value)
        for i in rows:
            self.data.pop(i-rows.index(i))
        
    def __eq__(self, value):
        '''return table of all value meeting operand =='''
        time=datetime.datetime.now()
        rows=self.__find_compare__("==", value)
        table_data=[self.columns]
        for row in rows:
            table_data.append(self.data[row])
        return table(self.database, f"pydb_{time}", True, table_data)
    
    def __ne__(self, value):
        '''return table of all value meeting operand !='''
        time=datetime.datetime.now()
        rows=self.__find_compare__("!=", value)
        table_data=[self.columns]
        for row in rows:
            table_data.append(self.data[row])
        return table(self.database, f"pydb_{time}", True, table_data)
    
    def __lt__(self, value):
        '''return table of all value meeting operand <'''
        time=datetime.datetime.now()
        rows=self.__find_compare__("<", value)
        table_data=[self.columns]
        for row in rows:
            table_data.append(self.data[row])
        return table(self.database, f"pydb_{time}", True, table_data)
    
    def __le__(self, value):
        '''return table of all value meeting operand <='''
        time=datetime.datetime.now()
        rows=self.__find_compare__("<=", value)
        table_data=[self.columns]
        for row in rows:
            table_data.append(self.data[row])
        return table(self.database, f"pydb_{time}", True, table_data)
    
    def __gt__(self, value):
        '''return table of all value meeting operand >'''
        time=datetime.datetime.now()
        rows=self.__find_compare__(">", value)
        table_data=[self.columns]
        for row in rows:
            table_data.append(self.data[row])
        return table(self.database, f"pydb_{time}", True, table_data)
    
    def __ge__(self, value):
        '''return table of all value meeting operand >='''
        time=datetime.datetime.now()
        rows=self.__find_compare__(">=", value)
        table_data=[self.columns]
        for row in rows:
            table_data.append(self.data[row])
        return table(self.database, f"pydb_{time}", True, table_data)