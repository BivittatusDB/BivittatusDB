#metaclasses to compare types used in joins and transaction management
# Define a custom metaclass for table
class TableMeta(type):
    def __new__(cls, name, bases, dct):
        namespace = {}
        namespace.update(dct)
        return type.__new__(cls, name, bases, namespace)
    
# Define a custom metaclass for SAVEPOINT
class SavepointMeta(type):
    def __new__(cls, name, bases, dct):
        namespace = {}
        namespace.update(dct)
        return type.__new__(cls, name, bases, namespace)

# Define a custom metaclass for ROLLBACK
class RollbackMeta(type):
    def __new__(cls, name, bases, dct):
        namespace = {}
        namespace.update(dct)
        return type.__new__(cls, name, bases, namespace)
    
# Define a custom metaclass for COMMIT
class CommitMeta(type):
    def __new__(cls, name, bases, dct):
        namespace = {}
        namespace.update(dct)
        return type.__new__(cls, name, bases, namespace)
    

# This next section is used to make errors. for the most part just follow the design inside the class
# class <ExceptionName>(Exception): ...
class BDBException:
    class ReadError(Exception): ... #For problems reading a file
    class EditError(Exception): ... #For Problems Editing a file
    class DeletionError(Exception): ... #For Problems Deleting a file
    class CreationError(Exception): ... #For problems Making a file
    class IOError(Exception): ... #For problems finding a file
    class ImportError(Exception): ... #for problems importing code
    class EncryptionError(Exception): ... # for problems with encryption/decryption
    class AggregateError(Exception): ... #for problems using aggregate functions
    class ColumunError(Exception): ... #for when column is not specified for dependant functions
    class EmptyTableError(Exception): ... #for when you try to loop through or get data from an empty table
    class StructureError(Exception): ... #Used in checks when structure doesn't match metadata
    class TypeError(Exception): ... #Used in checks when data types don't match metadata
    class KeyError(Exception): ... #Used when there is a problem with foreign or primary keys
    class RefError(Exception): ... #Used when refrenced table is not found
    class TransactionError(Exception): ... #Used for transaction management