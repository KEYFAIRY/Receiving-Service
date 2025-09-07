from typing import List
from beanie import Document
from app.infrastructure.database.models.practice_document import PracticeDocument

class UserDocument(Document):
    uid: str
    practices: List[PracticeDocument]

    class Settings:
        name = "users"  # Mongo collection name
