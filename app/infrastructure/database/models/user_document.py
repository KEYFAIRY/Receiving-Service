from typing import List
from app.infrastructure.database.models.practice_document import PracticeDocument
from beanie import Document


class UserDocument(Document):
    uid: str
    practices: List[PracticeDocument]

    class Settings:
        name = "users"  # Mongo collection name
