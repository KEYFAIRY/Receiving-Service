# app/domain/repositories/i_video_repo.py
from abc import ABC, abstractmethod
from typing import Protocol


class IVideoRepo(ABC):
    """Abstract repository interface for storing videos."""

    @abstractmethod
    async def save(self, filename: str, content: bytes) -> str:
        """
        Saves the video content and return the path where it was stored.
        """
        pass
