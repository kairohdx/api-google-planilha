
from typing import Any

from app.settings import Settings


class DbData:
    collection: Any
    db: Any | None = None

    def __init__(self, collectionName):
        settings = Settings()
        self.db = settings.db
        self.collection =  self.db[collectionName]
