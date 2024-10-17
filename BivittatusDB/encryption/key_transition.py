import os
from encrypt import RSAFileEncryptor

class KeyTransition:
    def __init__(self, database:str) -> None:
        self.path=database
        self.rsa=RSAFileEncryptor(self.path)

    def __copy_pubKey__(self):
        with open(f"{self.path}/private.pem", "rb") as original:
            with open(f"{self.path}/key.priv", "wb") as copy:
                copy.write(original.read())

    def ReKey(self, regen:bool=False):
        #used to generate new keys for a database
        if regen==True:
            self.__copy_pubKey__()
            self.rsa.generate_keys()
            self.priv_key=f"{self.path}/key.priv"
            self.rsa.private_key=self.rsa.key_manager.load_private_key(self.priv_key)
            self.rsa.public_key=self.rsa.key_manager.load_public_key()
        for file in os.listdir(self.path):
            if ".pydb" in file:
                self.rsa.decrypt_file(self.path+"/"+file)
                self.rsa.encrypt_file(self.path+"/"+file)
        self.rsa.private_key=self.rsa.key_manager.load_private_key()
    
    def export_table(self, table_name:str, export_key:str):
        "re-encrypt a table with a given public key, so that you don't need to share your private key"
        self.rsa.public_key=self.rsa.key_manager.load_public_key(export_key)
        self.rsa.decrypt_file(f"{self.path}/{table_name}.pydb")
        os.makedirs(f"{self.path}_export", exist_ok=True)
        self.rsa.encrypt_file(f"{self.path}/{table_name}.pydb", f"{self.path}_export/{table_name}.pydb")
        self.rsa.public_key=self.rsa.key_manager.load_public_key()
        self.rsa.encrypt_file(f"{self.path}/{table_name}.pydb")

    def import_table(self, table_path:str, import_key:str):
        'import a table that has been shared with you via Share.export_table, if you are the private key holder'
        _, filename = os.path.split(table_path)
        self.rsa.private_key=self.rsa.key_manager.load_private_key(import_key)
        self.rsa.decrypt_file(table_path)
        self.rsa.encrypt_file(table_path, f"{self.path}/{filename}")
        self.rsa.private_key=self.rsa.key_manager.load_private_key()
