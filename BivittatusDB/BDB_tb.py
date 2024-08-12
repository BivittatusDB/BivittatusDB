import metaclass
from traceback import print_exc as trace
try:     
    import datetime, BDB_metadata
    from bdb_aggregate import infomessage
    from encrypt import KeyManager
    from metaclass import *
    from bdb_foreign import ForeignKey, json
    from ast import literal_eval
except:
    raise metaclass.BDBException.ImportError(f"Could not import needed files in {__file__}")

class table(metaclass=TableMeta): ...

class table(metaclass=TableMeta):
    def __init__(self, handler:KeyManager, database, table_name, temp:bool=False, temp_data:list=None) -> table:
        self.io=handler
        self.autocommit=False
        self.database=database
        self.table_name=table_name
        self.temp=temp
        self.data = None  
        if self.temp==False:
            self.__read__()
        else:
            self.data=temp_data
            self.columns=self.data.pop(0)

    def __try_commit__(self):
        '''is autocommit turned on, it will save the table when a change is made.'''
        if self.autocommit:
            self.__save__()

    def __conv_list_dict__(self):
        '''convert data to a dictionary for joins'''
        return [dict(zip(self.columns, row)) for row in self.data]
    
    def __conv_dict_list__(self, dicts:dict, other):
        '''convert data back to a list after joins'''
        joined_cols = self.columns + [col for col in other.columns if col not in self.columns]
        return [joined_cols]+[[row.get(col, None) for col in joined_cols] for row in dicts]

    def __read__(self):
        '''Read data from a file'''
        try:
            self.data=self.io.ReadTable(self.table_name)
            self.columns=self.data.pop(0)
        except:
            infomessage(trace())
            raise BDBException.ReadError(f"Courld not read table {self.table_name}")

    def __edit__(self):
        '''Change data in database table. Used in the __save__ method'''
        try:
            data=[self.columns]+self.data
            self.io.UpdateTable(self.table_name, data)
        except:
            infomessage(trace())
            raise BDBException.EditError(f"Could not update table {self.table_name}")

    def __make__(self):
        try:
            metadata=[("Data", "Type")]
            for column, value in zip(self.columns, self.types):
                metadata.append((column, value))
            self.io.CreateTable(self.table_name, [self.columns], metadata)
            return table(self.io, self.database, self.table_name)
        except:
            infomessage(trace())
            raise BDBException.CreationError(f"Could not create table {self.table_name}")

    def __save__(self, name=None, types=None):
        try:
            '''Rename a database or save a temp database with a usable name.'''
            if name and types:
                self.temp=False
                self.table_name=name
                self.types=types
                new=self.__make__()
                new.data=self.data
                new.__save__()
                return new
        except Exception:
            infomessage(trace())
            return f"Error saving database"
        
        '''Commit changes to database. Call using save function in main file'''
        if name==None or name==self.table_name:
            self.temp=False
            self.__edit__()

    def __repr__(self) -> list:
        '''return raw data. Call with repr(self)'''
        return self.__read__()
    
    def __str__(self) -> str:
        '''return formatted data. Call using print(self)'''
        if not self.data or not self.columns:
            return "No data to show."
        try:
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
        except Exception as e:
            infomessage(trace())
            return f"Error generating the string representation of the table: {e}"
 
    def __load_metadata__(self):
        '''Load metadata from database. Used to make checks'''
        self.meta=BDB_metadata.table(self.io, self.database, self.table_name)
        return self.meta
    
    def __load_refrenced__(self):
        meta=self.__load_metadata__()
        key=meta[1].column.pop(-1)
        if key=="":
            return None
        key=json.loads(key)
        fkey=ForeignKey(*key)
        return fkey, table(self.io, self.database, fkey.FT)

    def __len__(self)->int:
        '''return the number of values in the data'''
        return len(self.data)
    
    def __fix_index__(self, key: int | str)->int:
        '''turns a str index into a int for proper management'''
        if type(key)==type(str()):
            return self.columns.index(key)
        return key

    def __getitem__(self, key: int | str):
        '''return a column from the data. Requirement to compare data'''
        self.column=[]
        data=self.data
        self.key=self.__fix_index__(key)
        for row in data:
            self.column.append(row[self.key])
        return self
    
    def __setitem__(self, key: int | str, value: any):
        '''change column name. Will probably change later.'''
        #text keys needed for update or else foreign keys don't work [PLAN FIX]
        org_key=key
        key=self.__fix_index__(key)
        try:
            value[1] == None
            data_to_change=self.data
        except AttributeError:
            data_to_change=value[1].data
        for row in self.data:
            if row in data_to_change:
                new_row=list(row)
                new_row[key] = value[0]
                self.data[self.data.index(row)] = tuple(new_row)
        ref=self.__load_refrenced__()
        if ref!=None:
            fkey, ft=ref
            ft@True
            if org_key==fkey.FC:
                ft[fkey.LC]=(value[0], ft[fkey.FC]==self.value)
                ft.__try_commit__()
        self.__try_commit__()

    def __empty_check__(self):
        if len(self) == 0:
            infomessage(trace())
            raise metaclass.BDBException.EmptyTableError(f"Can't use emptpy table {self.table_name}")

    def __iter__(self):
        '''start iterations. Call using `for item in self`'''
        self.__empty_check__()
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
        
    def __contains__(self, item: any):
        '''checks to see if item is in data. Call using `item in self`'''
        self.__empty_check__()
        if not self.column and self.data:
            infomessage(trace())
            raise BDBException.ColumunError("Must index a column to search item")
        if item in self.column:
            del self.column
            return True
        del self.column
        return False
    
    def __mul__(self, key: int | str):
        '''sort a the data by specified column (key). call using self*key (0 indexed)'''
        self.__empty_check__()
        key=self.__fix_index__(key)
        self.data=sorted(self.data, key=lambda x: x[key])
        self.__try_commit__()
        return self

    def __check_type__(self, new_data: tuple)->bool:
        '''Check new rows against specified datatypes'''
        data_types=self.__load_metadata__()[1].column
        if (len(data_types)-3) != (len(new_data)):
            infomessage(trace())
            raise metaclass.BDBException.StructureError(f"new data doesn't match table structure")
        for i in range(len(new_data)):
            if type(data_types[i]) != type(new_data[i]) and type(new_data[i]) != type(None):
                infomessage(trace())
                raise metaclass.BDBException.TypeError(f"New data does not match defined datatypes.")
        return True

    def __check_primary__(self, new_data: tuple)->bool:
        '''ensure primary key integrity'''
        key=self.__fix_index__(self.__load_metadata__()[1].column.pop(-3))
        if new_data[key] in self[key].column:
            infomessage(trace())
            raise metaclass.BDBException.KeyError(f"primary key {new_data[key]} is already in primary key")
        return True
    
    def __load_foreign__(self, other: str):
        other=table(self.io, self.database, other)
        return other

    def __check_foreign__(self, new_data:tuple)->bool:
        '''Ensure new data fits the foreign key constraints'''
        meta=self.__load_metadata__()
        if meta[1].column.pop(-2) == "None":
            return True
        key=self.__fix_index__(meta[1].column.pop(-3))
        other_name=literal_eval(self.__load_metadata__()[1].column.pop(-2))[0]
        other=self.__load_foreign__(other_name)
        other_key = other.__fix_index__(other.__load_metadata__()[1].column.pop(-3))
        if new_data[key] in other[other_key]:
            return True
        else:
            infomessage(trace())
            raise metaclass.BDBException.RefError(f"Value {new_data[key]} not found in {other_name}")

    def __add__(self, value:tuple)->None:
        '''add new row to the table. call using self+value'''
        if self.__check_type__(value) and self.__check_primary__(value) and self.__check_foreign__(value):
            self.data.append(value)
        self.__try_commit__()

    def __find_compare__(self, operator:str, value):
        self.value=value
        '''used to remove all data not meeting opperator requirments.'''
        self.__empty_check__()
        if not self.column:
            infomessage(trace())
            raise BDBException.ColumunError(f"Must Index Column to use comparison {operator}")
        data=self.column
        rows=[]
        for i in range(len(data)):
            if eval(f"data[i]{operator}value"):
                rows.append(i)
        return rows
    
    def __sub__(self, value: any):
        '''remove all rows containing value in specified column'''
        rows=self.__find_compare__("==", value)
        for i in rows:
            self.data.pop(i-rows.index(i))
        self.__try_commit__()
        
    def __eq__(self, value):
        '''return table of all value meeting operand =='''
        time=datetime.datetime.now()
        rows=self.__find_compare__("==", value)
        table_data=[self.columns]
        for row in rows:
            table_data.append(self.data[row])
        return table(self.io, self.database, f"pydb_{time}", True, table_data)
    
    def __ne__(self, value):
        '''return table of all value meeting operand !='''
        time=datetime.datetime.now()
        rows=self.__find_compare__("!=", value)
        table_data=[self.columns]
        for row in rows:
            table_data.append(self.data[row])
        return table(self.io, self.database, f"pydb_{time}", True, table_data)
    
    def __lt__(self, value):
        '''return table of all value meeting operand <'''
        time=datetime.datetime.now()
        rows=self.__find_compare__("<", value)
        table_data=[self.columns]
        for row in rows:
            table_data.append(self.data[row])
        return table(self.io, self.database, f"pydb_{time}", True, table_data)
    
    def __le__(self, value):
        '''return table of all value meeting operand <='''
        time=datetime.datetime.now()
        rows=self.__find_compare__("<=", value)
        table_data=[self.columns]
        for row in rows:
            table_data.append(self.data[row])
        return table(self.io, self.database, f"pydb_{time}", True, table_data)
    
    def __gt__(self, value):
        '''return table of all value meeting operand >'''
        time=datetime.datetime.now()
        rows=self.__find_compare__(">", value)
        table_data=[self.columns]
        for row in rows:
            table_data.append(self.data[row])
        return table(self.io, self.database, f"pydb_{time}", True, table_data)
    
    def __ge__(self, value):
        '''return table of all value meeting operand >'''
        time=datetime.datetime.now()
        rows=self.__find_compare__(">=", value)
        table_data=[self.columns]
        for row in rows:
            table_data.append(self.data[row])
        return table(self.io, self.database, f"pydb_{time}", True, table_data)
    
    def __lshift__(self, other):
        '''left join tables. call using table1<<table2'''
        self.__empty_check__()
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
        return table(self.io, self.database, f"pydb_{time}", True, joined_table)

    def __rshift__(self, other):
        '''right join tables. Call using table1>>table2'''
        self.__empty_check__()
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
        return table(self.io, self.database, f"pydb_{time}", True, joined_table)

    def __xor__(self, other):
        '''full join tables. Call using table1^table2'''
        self.__empty_check__()
        time=datetime.datetime.now()
        ljoin = (self << other).__conv_list_dict__()
        rjoin = (self >> other).__conv_list_dict__()
        full_join = {tuple(row.items()): row for row in ljoin+rjoin}.values()
        full_join = self.__conv_dict_list__(full_join, other)
        return table(self.io, self.database, f"pydb_{time}", True, full_join)
    
    def __matmul__(self, bool):
        '''set autocommit. call using table@bdb.ON or table@bdb.OFF'''
        self.autocommit=bool

    def __rmatmul__(self, other):
        if type(other)==type(SAVEPOINT):
            SAVEPOINT.__matmul__(other, self)
        elif type(other)==type(ROLLBACK):
            ROLLBACK.__matmul__(other, self)
        elif type(other)==type(COMMIT):
            COMMIT.__matmul__(other, self)

    def __scan__(self):
        for row in self.data:
            if self.__check_foreign__(row) and self.__check_type__(row) and self.__scan_primary__():
                continue

    def contains_duplicates(self, lst):
        for i in range(len(lst)):
            for j in range(i + 1, len(lst)):
                if lst[i] == lst[j]:
                    return True
        return False

    def __scan_primary__(self):
        key=self.__fix_index__(self.__load_metadata__()[1].column.pop(-3))
        if self.contains_duplicates(self[key].column):
            infomessage(trace())
            raise metaclass.BDBException.KeyError(f"primary key is duplicated in {self.table_name}: {self.column}")
        return True
    
    def __invert__(self):
        self.__init__(self.io, self.database, self.table_name,self.temp, self.data)
        return self

class SAVEPOINT(metaclass=SavepointMeta):
    def __matmul__(self, other:table):
        try:
            data=[other.columns] + other.data
            rollback=table(other.io, other.database, "rollback"+other.table_name, True, data)
            other.rollback = rollback
        except:
            infomessage(trace())
            raise metaclass.BDBException.TransactionError(f"Error creating savepoint for {other.table_name}")

class ROLLBACK(metaclass=RollbackMeta):
    def __matmul__(self, other:table):
        if not other.rollback:
            infomessage(trace())
            raise metaclass.BDBException.TransactionError(f"Table {other.table_name} doesn't have a savepoint")
        try:
            data=other.rollback.data
            del other.rollback.data
            other.data=data
        except:
            infomessage(trace())
            raise metaclass.BDBException.TransactionError(f"Error Rolling back table {other.table_name}")

class COMMIT(metaclass=CommitMeta):
    def __matmul__(self, other:table):
        other.__save__()