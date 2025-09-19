import os
import aiofiles
import logging
from app.domain.repositories.i_videos_repo import IVideoRepo

logger = logging.getLogger(__name__)

class LocalVideoRepository(IVideoRepo):
    """Concrete implementation of IVideoRepo using local file system."""
    
    def __init__(self, base_dir: str | None = None):
        self.base_dir = base_dir or os.getenv("CONTAINER_VIDEO_PATH", "/tmp/videos")
        os.makedirs(self.base_dir, exist_ok=True)

    async def save(self, filename: str, content: bytes, uid: str) -> str:
        """
        Save video under path: base_dir/{uid}/videos/{filename}
        """
        user_dir = os.path.join(self.base_dir, uid, "videos")
        os.makedirs(user_dir, exist_ok=True)  # Create dirs if not exists

        file_path = os.path.join(user_dir, filename)
        try:
            async with aiofiles.open(file_path, "wb") as out_file:
                await out_file.write(content)
            logger.info(f"Video saved at {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"Error saving video: {e}", exc_info=True)
            raise
