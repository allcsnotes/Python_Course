from sqlalchemy import event


class QueryCounter:
    """Counts the queries sent to the database."""

    def __init__(self, engine):
        self.count = 0
        event.listen(engine, "before_cursor_execute", self._hit)

    def _hit(self, *args):
        self.count += 1
