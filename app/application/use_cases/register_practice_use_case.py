from app.application.dto.practice_dto import PracticeDTO
from app.application.dto.practice_metadata_dto import PracticeMetadataDTO
from app.domain.entities.practice import Practice
from app.domain.services.practice_service import PracticeService
from app.infrastructure.kafka.kafka_message import KafkaMessage
from app.infrastructure.kafka.kafka_producer import KafkaProducer
from app.core.exceptions import DatabaseConnectionException, ValidationException
from app.core.config import settings

import logging

logger = logging.getLogger(__name__)


class RegisterPracticeUseCase:
    """Use case to save practice video and metadata"""

    def __init__(self, practice_service: PracticeService, kafka_producer: KafkaProducer):
        self.practice_service = practice_service
        self.kafka_producer = kafka_producer

    async def execute(self, data: PracticeDTO, video_content: bytes) -> str:
        try:
            # 1. Store practice data
            # DTO -> Entity
            practice = Practice(
                date=data.date,
                time=data.time,
                num_musical_errors=0,
                num_postural_errors=0,
                duration=data.duration,
                id_student=data.uid,
                scale=data.scale,
                scale_type=data.scale_type,
                bpm=data.bpm,
            )
            
            practice_metadata = await self.practice_service.store_practice_data(practice=practice, video_content=video_content, video_in_local=data.video_local_route)
            
            logging.info(f"Practice data stored successfully for practice ID {practice_metadata.id} in local path {practice_metadata.video_in_server}")
            
            # 2. Publish Kafka event (send message about new practice registered)
            kafka_message = KafkaMessage(
                uid=data.uid,
                practice_id=practice_metadata.id,
                message="New practice registered",
                scale=data.scale,
                scale_type=data.scale_type,
                video_route=practice_metadata.video_in_server,
                reps=data.reps,
                bpm=data.bpm,
            )
            
            logging.info(f"Publishing Kafka message for practice ID {practice_metadata.id} to topic {settings.KAFKA_OUTPUT_TOPIC}")
            
            await self.kafka_producer.publish_message(topic=settings.KAFKA_OUTPUT_TOPIC, message=kafka_message)

            return practice_metadata.video_in_server
        except (DatabaseConnectionException, ValidationException) as e:
            logger.error(f"Error while registering practice: {e}", exc_info=True)
            raise
