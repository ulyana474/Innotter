from enum import Enum

class PageMessageAction(Enum):
    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'
    NAME = 'action'
    KEY_PAGE_ID = 'page_id'
    FIELD = 'field'
    INCREASE = 'increase'

    def __str__(self):
        return self.value