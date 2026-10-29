from app.store import Store

STORE = Store()


def get_store() -> Store:
    return STORE
