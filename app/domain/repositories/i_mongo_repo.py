from abc import ABC, abstractmethod
from app.domain.entities.practice import Practice


class IMongoRepo(ABC):
    """Abstract repository for managing Practice documents in MongoDB."""

    @abstractmethod
    async def add_practice_to_user(self, uid: str, practice: Practice) -> Practice:
        """Adds a new practice to a user identified by UID."""
        pass
