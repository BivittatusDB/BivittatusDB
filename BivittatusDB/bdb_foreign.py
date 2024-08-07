import BDB_metadata, json

class ForeignKey(list):
    def __init__(self, ForeignTable, ForeignColumn, LocalColumn) -> None:
        self.FT, self.FC, self.LC=ForeignTable, ForeignColumn, LocalColumn
        super().__init__()

    def __repr__(self) -> str:
        return json.dumps([self.FT,self.FC, self.LC])