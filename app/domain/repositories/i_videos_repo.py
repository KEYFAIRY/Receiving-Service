from abc import ABC, abstractmethod

class IVideoRepo(ABC):
    """Abstract repository interface for storing videos."""

    @abstractmethod
    async def save(self, filename: str, content: bytes, uid: str) -> str:
        """
        Saves the video content and return the path where it was stored.
        """
        pass
