import logging
from app.domain.entities.practice import Practice
from app.domain.entities.practice_metadata import PracticeMetadata
from app.domain.entities.scale import Scale
from app.domain.repositories.i_metadata_repo import IMetadataRepo
from app.domain.repositories.i_practice_repo import IPracticeRepo
from app.domain.repositories.i_scale_repo import IScaleRepo
from app.domain.repositories.i_videos_repo import IVideoRepo

logger = logging.getLogger(__name__)


class PracticeService:
    """Domain service for management of practice data"""

    def __init__(self, practice_repo: IPracticeRepo, scale_repo: IScaleRepo, metadata_repo: IMetadataRepo, videos_repo: IVideoRepo):
        self.practice_repo = practice_repo
        self.scale_repo = scale_repo
        self.metadata_repo = metadata_repo
        self.videos_repo = videos_repo

    async def store_practice_data(self, practice: Practice, video_content: bytes, video_in_local:str) -> PracticeMetadata:
        """
        Orchestrates storing of practice data:
        - Save the video in storage
        - Save metadata in MySQL
        - Save extended metadata in Mongo
        """

        # 1. Save practice data in MySQL
        
        # Check if scale exists, if not create it
        id_scale = None
        
        existing_scale = await self.scale_repo.get_by_name_and_type(practice.scale, practice.scale_type)
        
        if not existing_scale:
            scale = Scale(name=practice.scale, scale_type=practice.scale_type)
            new_scale = await self.scale_repo.create(scale)
            id_scale = new_scale.id
        else:
            id_scale = existing_scale.id
            
        practice.id_scale = id_scale
            
        mysql_saved_practice = await self.practice_repo.create(practice)
        
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
        
        await self.metadata_repo.add_practice_to_user(practice.id_student, practice_metadata)
        
        logging.info(f"Practice metadata saved in Mongo for practice ID {practice_metadata.id}")
        
        return practice_metadata