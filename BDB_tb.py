import BDB_io as io, json, datetime, BDB_metadata

class table:
    def __init__(self, database, table_name, temp:bool=False, temp_data:list=None) -> None:
        self.autocommit=False
        self.database=database
        self.table_name=table_name
        self.temp=temp
        if self.temp==False:
            self.__read__()
        else:
            self.data=temp_data
            self.columns=self.data.pop(0)

    def __conv_list_dict__(self):
        return [dict(zip(self.columns, row)) for row in self.data]
    
    def __conv_dict_list__(self, dicts:dict, other):
        joined_cols = self.columns + [col for col in other.columns if col not in self.columns]
        return [joined_cols]+[[row.get(col, None) for col in joined_cols] for row in dicts]

    def __read__(self):
        '''Read data from a file'''
        reader=io.read(self.database)
        self.data=json.loads(reader.read_table(self.table_name))
        self.columns=self.data.pop(0)

    def __write__(self, new_table):
        '''Write a new table to database. Not used currently'''
        writer=io.write(self.database)
        data=json.dumps([self.columns]+[self.data])
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
    
    def __load_metadata__(self):
        '''Load metadata from database. Used to make checks'''
        return BDB_metadata.table(self.database, self.table_name)

    def __len__(self)->int:
        '''return the number of values in the data'''
        return len(self.data)
    
    def __fix_index__(self, key)->int:
        '''turns a str index into a int for proper management'''
        if type(key)==type(str()):
            return self.columns.index(key)
        return key

    def __getitem__(self, key: str):
        '''return a column from the data. Requirement to compare data'''
        self.column=[]
        data=self.data
        self.key=self.__fix_index__(key)
        for row in data:
            self.column.append(row[self.key])
        return self
    
    def __setitem__(self, key, value):
        '''change column name. Will probably change later.'''
        self.columns[key]=value

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
        if not self.column and self.data:
            raise IndexError("Must index a column to search item")
        if item in self.column:
            del self.column
            return True
        del self.column
        return False
    
    def __mul__(self, key:int):
        '''sort a the data by specified column (key). call using self*key (0 indexed)'''
        self.data=sorted(self.data, key=lambda x: x[key])
        return self

    def __check_type__(self, new_data: tuple)->bool:
        '''Check new rows against specified datatypes'''
        data_types=self.__load_metadata__()[1].column
        if (len(data_types)-1) != (len(new_data)):
            raise SyntaxError(f"new data doesn't match table structure")
        for i in range(len(new_data)):
            if type(data_types[i]) != type(new_data[i]):
                raise SyntaxError(f"New data doesn't match table structure")
        return True

    def __check_primary__(self, new_data: tuple)->bool:
        '''ensure primary key integrity'''
        key=self.__fix_index__(self.__load_metadata__()[1].column.pop(-1))
        if new_data[key] in self[key]:
            raise ValueError(f"primary key {new_data[key]} is already in primary key")
        return True  

    def __add__(self, value:list):
        '''add new row to the table. call using self+value'''
        if self.__check_type__(value) and self.__check_primary__(value):
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
        '''return table of all value meeting operand >'''
        time=datetime.datetime.now()
        rows=self.__find_compare__(">=", value)
        table_data=[self.columns]
        for row in rows:
            table_data.append(self.data[row])
        return table(self.database, f"pydb_{time}", True, table_data)
    
    def __lshift__(self, other):
        time=datetime.datetime.now()
        left_table=self.__conv_list_dict__()
        left_cols =self.columns
        join_key_left=self.columns[self.key]
        right_table=other.__conv_list_dict__()
        right_cols=other.columns
        join_key_right=other.columns[other.key]

        right_dict= {row[join_key_right]:row for row in right_table}
        joined_table=[]
        for left_row in left_table:
            key= left_row[join_key_left]
            matched_row=right_dict.get(key, {})
            combine_row={**left_row, **{col:matched_row.get(col, None) for col in right_cols if col not in left_cols}}
            joined_table.append(combine_row)
        joined_table=self.__conv_dict_list__(joined_table, other)
        return table(self.database, f"pydb_{time}", True, joined_table)

    def __rshift__(self, other):
        time=datetime.datetime.now()
        left_table=self.__conv_list_dict__()
        left_cols =self.columns
        join_key_left=self.columns[self.key]
        right_table=other.__conv_list_dict__()
        right_cols=other.columns
        join_key_right=other.columns[other.key]

        left_dict = {row[join_key_left]:row for row in left_table}
        joined_table=[]
        
        for right_row in right_table:
            key=right_row[join_key_right]
            matched_row = left_dict.get(key, {})
            combined_row = {**{col: matched_row.get(col, None) for col in left_cols if col not in right_cols}, **right_row}
            joined_table.append(combined_row)
        joined_table=self.__conv_dict_list__(joined_table, other)
        return table(self.database, f"pydb_{time}", True, joined_table)

    def __xor__(self, other):
        time=datetime.datetime.now()
        ljoin = (self << other).__conv_list_dict__()
        rjoin = (self >> other).__conv_list_dict__()
        full_join = {tuple(row.items()): row for row in ljoin+rjoin}.values()
        full_join = self.__conv_dict_list__(full_join, other)
        return table(self.database, f"pydb_{time}", True, full_join)
    
    def __matmul__(self, bool):
        self.autocommit=bool