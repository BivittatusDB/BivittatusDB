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