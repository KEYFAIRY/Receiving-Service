from abc import ABC, abstractmethod
from app.domain.entities.practice import Practice
from app.domain.entities.practice_metadata import PracticeMetadata

class IMetadataRepo(ABC):
    """Abstract repository for managing Practice documents in MongoDB."""

    @abstractmethod
    async def add_practice_to_user(self, uid: str, practice: Practice) -> Practice:
        """Adds a new practice to a user identified by UID."""
        pass
    
    @abstractmethod
    async def get_by_uid_and_practice_id(self, uid: str, practice_id: int) -> PracticeMetadata | None:
        """Fetches practice metadata for a user identified by UID and practice ID."""
        pass
