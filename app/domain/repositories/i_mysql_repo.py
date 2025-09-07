from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.practice import Practice


class IMySQLRepo(ABC):
    """Abstract repository interface for Practice entity."""

    @abstractmethod
    async def create(self, practice: Practice) -> Practice:
        """Creates a new practice."""
        pass
