from functools import lru_cache

from fastapi import Request

from app.application.use_cases.register_practice_use_case import RegisterPracticeUseCase
from app.domain.services.practice_service import PracticeService
from app.infrastructure.repositories.local_video_repo import LocalVideoRepository
from app.infrastructure.repositories.mongo_metadata_repo import MongoMetadataRepository
from app.infrastructure.repositories.mysql_practice_repo import MySQLPracticeRepository
from app.infrastructure.repositories.mysql_scale_repo import MySQLScaleRepository

# Repositories
@lru_cache()
def get_mysql_practice_repository() -> MySQLPracticeRepository:
    """Get instance of MySQLPracticeRepository."""
    return MySQLPracticeRepository()

@lru_cache()
def get_mysql_scale_repository() -> MySQLScaleRepository:
    """Get instance of MySQLScaleRepository."""
    return MySQLScaleRepository()

@lru_cache()
def get_mongo_practice_repository() -> MongoMetadataRepository:
    """Get instance of MongoMetadataRepository."""
    return MongoMetadataRepository()

@lru_cache()
def get_local_video_repository() -> LocalVideoRepository:
    """Get instance of LocalVideoRepository."""
    return LocalVideoRepository() 

# Services
@lru_cache()
def get_register_practice_service() -> PracticeService:
    """Get instance of PracticeService."""
    return PracticeService(
        practice_repo=get_mysql_practice_repository(),
        scale_repo=get_mysql_scale_repository(),
        metadata_repo=get_mongo_practice_repository(),
        videos_repo=get_local_video_repository()
    )
    
# Use Cases
@lru_cache()
def get_register_practice_use_case() -> RegisterPracticeUseCase:
    """Get instance of RegisterPracticeUseCase."""
    return RegisterPracticeUseCase(
        practice_service=get_register_practice_service(),
        kafka_producer=None
    )
    

# FastAPI Dependencies
def register_practice_use_case_dependency(request: Request) -> RegisterPracticeUseCase:
    """Dependency to get RegisterPracticeUseCase instance with KafkaProducer from app.state"""
    kafka_producer = request.app.state.kafka_producer

    return RegisterPracticeUseCase(
        practice_service=get_register_practice_service(),
        kafka_producer=kafka_producer,
    )