import h5py, gzip, json, os
from binascii import hexlify, unhexlify

class HDF5Handler:
    def __init__(self, filename:str, ext:str=".pydb") -> None:
        self.filename = filename
        self.ext = ext

    def open_file(self, mode):
        return h5py.File(self.filename + self.ext, mode)

    def read_table(self, table_name):
        with self.open_file("r") as infile:
            data = infile[f'/{table_name}'][()]
            table_data = json.loads(gzip.decompress(unhexlify(data)).decode())
            infile.close()
        return table_data

    def write_table(self, table_name:str, data:str):
        with self.open_file("w") as outfile:
            data = hexlify(gzip.compress(json.dumps(data).encode()))
            outfile.create_dataset(f"/{table_name}", data=data)
            outfile.close()

    def edit_table(self, table_name:str, new_data):
        with self.open_file("a") as editfile:
            new_data = hexlify(gzip.compress(json.dumps(new_data).encode()))
            editfile[f'/{table_name}'][()] = new_data
            editfile.close()

if __name__=='__main__':
    handler = HDF5Handler("test")
    handler.write_table("testing", "hello world")

    print(handler.read_table("testing"))

    handler.edit_table("testing", "it worked")
    print(handler.read_table("testing"))
