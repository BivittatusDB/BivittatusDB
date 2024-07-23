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
    class ReadError(Exception): ...
    class EditError(Exception): ...
    class DeletionError(Exception): ...
    class CreationError(Exception): ...