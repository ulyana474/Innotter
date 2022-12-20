from enum import Enum

class PageMessageAction(Enum):
    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'
    NAME = 'action'

    def __str__(self):
        return self.value