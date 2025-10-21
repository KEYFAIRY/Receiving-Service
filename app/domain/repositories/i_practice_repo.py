from abc import ABC, abstractmethod
from datetime import datetime
from app.domain.entities.practice import Practice

class IPracticeRepo(ABC):
    """Abstract repository interface for Practice entity."""

    @abstractmethod
    async def create(self, practice: Practice) -> Practice:
        """Creates a new practice."""
        pass
    
    @abstractmethod
    async def get_by_datetime_uid_scale(self, datetime: datetime, uid: int, id_scale: int) -> Practice | None:
        """Retrieves an existing practice."""
        pass 
