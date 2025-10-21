import logging
from app.domain.entities.practice_metadata import PracticeMetadata
from app.domain.repositories.i_metadata_repo import IMetadataRepo
from app.infrastructure.database.models.user_document import UserDocument
from app.infrastructure.database.models.practice_document import PracticeDocument

logger = logging.getLogger(__name__)

class MongoMetadataRepository(IMetadataRepo):
    """Concrete implementation of IMetadataRepo using Beanie."""
    
    async def get_by_uid_and_practice_id(self, uid: str, practice_id: int) -> PracticeMetadata | None:
        user_doc = await UserDocument.find_one({"uid": uid})
        if not user_doc:
            return None

        # Search for the practice within the user's practices array
        practice_doc = None
        for practice in user_doc.practices:
            if practice.id_practice == practice_id:
                practice_doc = practice
                break
        
        if not practice_doc:
            return None

        return PracticeMetadata(
            id=practice_doc.id_practice,
            video_in_server=practice_doc.video_in_server,
            video_in_local=practice_doc.video_in_local,
            report=practice_doc.report,
            video_done=practice_doc.video_done,
            audio_done=practice_doc.audio_done,
        )

    async def add_practice_to_user(self, uid: str, practice: PracticeMetadata) -> PracticeMetadata:
        try:
            # Find user document
            user_doc = await UserDocument.find_one({"uid": uid})

            if not user_doc:
                user_doc = UserDocument(
                    uid=uid,
                    practices=[],
                )
                await user_doc.insert()
                logger.info(f"Created new user document for uid={uid}")

            # Convert Practice entity -> PracticeDocument
            practice_doc = PracticeDocument(
                id_practice=practice.id,
                video_in_server=practice.video_in_server,
                video_in_local=practice.video_in_local,
                report=practice.report,
                video_done=practice.video_done,
                audio_done=practice.audio_done,
            )

            # Append and save
            user_doc.practices.append(practice_doc)
            await user_doc.save()

            logger.info(f"Practice {practice.id} added to user {uid}")

            return practice  # return domain entity back

        except Exception as e:
            logger.error(f"Error adding practice to user {uid}: {e}", exc_info=True)
            raise
