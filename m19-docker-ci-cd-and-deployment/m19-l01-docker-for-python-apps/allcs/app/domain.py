class NotFound(Exception):
    def __init__(self, kind, item_id):
        self.kind = kind
        self.item_id = item_id


class Conflict(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message
