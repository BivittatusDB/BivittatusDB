import ctypes, encrypt, getpass, pathlib
from json import dumps, loads

io_lib = ctypes.CDLL("./lib_bdb.so")

class DBio_lib:
    def __init__(self, databasename:str, encrypted:bool=False) -> None:
        self.database=databasename+".pydb"
        self.dbname=ctypes.c_char_p((databasename+".pydb").encode())
        self.encrypted=encrypted
        if self.encrypted:
            self.key=getpass.getpass(f"Password for {databasename}: ").encode()
        if pathlib.Path(self.database).is_file():
            encrypt.File_Enc().dec(self.database, self.key)

    def __encode_data__(self, data):
        data=dumps(data).encode()
        return data
    
    def __decode_data__(self, data):
        return loads(data)
    
    def __encode_atrributes__(self, *args:bytes) ->tuple[ctypes.c_char_p]:
        encoded=[]
        for arg in args:
            encoded.append(ctypes.c_char_p(arg))
        return tuple(encoded)

    def CreateTable(self, tablename:str, data:str):
        data=self.__encode_data__(data)
        tablename, data= self.__encode_atrributes__(tablename.encode(), data)
        io_lib.CreateDataset(self.dbname, tablename, data)

    def ReadTable(self, tablename:str):
        tablename = self.__encode_atrributes__(tablename.encode())[0]
        io_lib.GetData.restype = ctypes.c_char_p
        return self.__decode_data__(io_lib.GetData(self.dbname, tablename).decode())
    
    def UpdateTable(self, tablename:str, new_data:str):
        new_data=self.__encode_data__(new_data)
        tablename, new_data = self.__encode_atrributes__(tablename.encode(), new_data)
        io_lib.UpdateData(self.dbname, tablename, new_data)

    def DeleteTable(self, tablename:str):
        tablename = self.__encode_atrributes__(tablename.encode())[0]
        io_lib.DeleteSet(self.dbname, tablename)
    
    def close_DB(self):
        if self.encrypted:
            encrypt.File_Enc().enc(self.database, self.key)

if __name__ == "__main__":
    handle=DBio_lib("Hello")
    table1=[["Columns1"], ["Row1"]]
    table2=[["Columns2"], ["Row2"]]
    table3=[["Columns3"], ["Row3"]]
    update=[["ColumnsU"], ["RowU"]]
    handle.CreateTable("Table1", table1)
    handle.CreateTable("Table2", table2)
    handle.CreateTable("Table3.00", table3)
    handle.UpdateTable("Table2", update)
    text=handle.ReadTable("Table2")
    handle.DeleteTable("Table1")
    print(text)

    handle.encrypted=True
    handle.key=b"Testing"
    del handle

    handle=DBio_lib("Hello", True)
    print(handle.ReadTable("Table2"))