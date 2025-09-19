from abc import ABC, abstractmethod
from app.domain.entities.scale import Scale

class IScaleRepo(ABC):
    """Abstract repository interface for Scale entity."""

    @abstractmethod
    async def create(self, scale: Scale) -> Scale:
        """Creates a new scale."""
        pass
    
    @abstractmethod
    async def get_by_name_and_type(self, name: str, scale_type: str) -> Scale | None:
        """Fetches a scale by its name and type."""
        pass
