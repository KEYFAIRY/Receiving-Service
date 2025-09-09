import logging
from app.domain.entities.practice import Practice
from app.domain.entities.practice_metadata import PracticeMetadata
from app.domain.repositories.i_mongo_repo import IMongoRepo
from app.domain.repositories.i_mysql_repo import IMySQLRepo
from app.domain.repositories.i_videos_repo import IVideoRepo

logger = logging.getLogger(__name__)


class PracticeService:
    """Domain service for management of practice data"""

    def __init__(self, mysql_repo: IMySQLRepo, mongo_repo: IMongoRepo, videos_repo: IVideoRepo):
        self.mysql_repo = mysql_repo
        self.mongo_repo = mongo_repo
        self.videos_repo = videos_repo

    async def store_practice_data(self, practice: Practice, video_content: bytes, video_in_local:str) -> PracticeMetadata:
        """
        Orchestrates storing of practice data:
        - Save the video in storage
        - Save metadata in MySQL
        - Save extended metadata in Mongo
        """

        # 1. Save practice data in MySQL
        mysql_saved_practice = await self.mysql_repo.create(practice)
        
        logging.info(f"Practice metadata saved in MySQL with ID {mysql_saved_practice.id}")
        
        # 2. Save the video on disk (via videos_repo)
        video_filename = f"practice_{mysql_saved_practice.id}.mp4"
        file_path = await self.videos_repo.save(video_filename, video_content, mysql_saved_practice.id_student)
        
        logging.info(f"Practice video saved at {file_path}")
        
        # 3. Save practice metadata in Mongo
        practice_metadata = PracticeMetadata(
            id=mysql_saved_practice.id,
            video_in_server=file_path,
            video_in_local=video_in_local,
            report="",
            video_done=False,
            audio_done=False,
        )
        
        await self.mongo_repo.add_practice_to_user(practice.id_student, practice_metadata)
        
        logging.info(f"Practice metadata saved in Mongo for practice ID {practice_metadata.id}")
        
        return practice_metadata