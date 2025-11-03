import logging
from app.application.dto.practice_dto import PracticeDTO
from app.domain.entities.practice import Practice
from app.domain.services.practice_service import PracticeService
from app.core.exceptions import DatabaseConnectionException, ValidationException
from app.core.config import settings
from app.messages.kafka_message import KafkaMessage
from app.messages.kafka_producer import KafkaProducer

logger = logging.getLogger(__name__)

class RegisterPracticeUseCase:
    """Use case to save practice video and metadata"""

    def __init__(self, practice_service: PracticeService, kafka_producer: KafkaProducer):
        self.practice_service = practice_service
        self.kafka_producer = kafka_producer

    async def execute(self, data: PracticeDTO, video_content: bytes) -> int:
        try:
            # DTO -> Entity
            practice = Practice(
                date=data.date,
                time=data.time,
                scale=data.scale,
                scale_type=data.scale_type,
                num_postural_errors=0,  # Placeholder, to be updated later
                num_musical_errors=0,   # Placeholder, to be updated later
                duration=data.duration,
                bpm=data.bpm,
                figure=data.figure,
                octaves=data.octaves,
                total_notes_played=data.total_notes_played,
                id_student=data.uid,
            )
            
            # 1. Check if practice already exists
            existent_practice = await self.practice_service.practice_exists(practice)
            
            if existent_practice is not None:
                logging.info(f"Practice already exists with ID {existent_practice.id}, skipping registration.")
                return existent_practice.id
            else:
                # 1. Store practice data
                practice_metadata = await self.practice_service.store_practice_data(practice=practice, video_content=video_content, video_in_local=data.video_local_route)
                
                logging.info(f"Practice data stored successfully for practice ID {practice_metadata.id} in local path {practice_metadata.video_in_server}")
                
                kafka_message = KafkaMessage(
                    uid=data.uid,
                    practice_id=practice_metadata.id,
                    date=data.date,
                    time=data.time,
                    message="New practice registered",
                    scale=data.scale,
                    scale_type=data.scale_type,
                    duration=data.duration,
                    bpm=data.bpm,
                    figure=data.figure,
                    octaves=data.octaves,
                )
                
                logging.info(f"Publishing Kafka message for practice ID {practice_metadata.id} to topic {settings.KAFKA_OUTPUT_TOPIC}")
                
                # 2. Publish Kafka event (send message about new practice registered)
                await self.kafka_producer.publish_message(topic=settings.KAFKA_OUTPUT_TOPIC, message=kafka_message)

                return practice_metadata.id
        except (DatabaseConnectionException, ValidationException) as e:
            logger.error(f"Error while registering practice: {e}", exc_info=True)
            raise