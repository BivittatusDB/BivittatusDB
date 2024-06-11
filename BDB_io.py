import h5py, gzip
from binascii import hexlify, unhexlify

class read:
    def __init__(self, filename:str, ext:str=".pydb") -> None:
        self.filename=filename
        self.ext=ext

    def read_table(self, table_name):
        self.infile=h5py.File(self.filename+self.ext, "r")
        data=self.infile[f'/{table_name}'][()]
        table_data=gzip.decompress(unhexlify(data))
        self.infile.close()
        return table_data
    
class write:
    def __init__(self, filename:str, ext:str=".pydb") -> None:
        self.filename=filename
        self.ext=ext

    def write_table(self, table_name:str, data:str):
        self.outfile=h5py.File(self.filename+self.ext, "w")
        data=hexlify(gzip.compress(data.encode()))
        self.outfile.create_dataset(f"/{table_name}", data=data)
        self.outfile.close()

class edit:
    def __init__(self, filename:str, ext:str=".pydb") -> None:
        self.filename=filename
        self.ext=ext

    def edit_table(self, table_name:str, new_data):
        new_data=hexlify(gzip.compress(new_data.encode()))
        self.editfile=h5py.File(self.filename+self.ext, "a")
        self.editfile[f'/{table_name}'][()]=new_data
        self.editfile.close()

if __name__=='__main__':
    writer=write("test")
    writer.write_table("testing", "hello world")

    reader=read("test")
    print(reader.read_table("testing"))

    editor=edit("test")
    editor.edit_table("testing", "it worked")
    print(reader.read_table("testing"))