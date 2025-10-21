import logging
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.core.exceptions import DatabaseConnectionException
from app.domain.entities.practice import Practice
from app.domain.repositories.i_practice_repo import IPracticeRepo
from app.infrastructure.database.models.practice_model import PracticeModel
from app.infrastructure.database.mysql_connection import mysql_connection

logger = logging.getLogger(__name__)

class MySQLPracticeRepository(IPracticeRepo):
    """Concrete implementation of IPracticeRepo for Practice using MySQL."""

    async def create(self, practice: Practice) -> Practice:
        async with mysql_connection.get_async_session() as session:
            try:
                practice_dt = datetime.strptime(
                    f"{practice.date} {practice.time}", "%Y-%m-%d %H:%M:%S"
                )

                model = PracticeModel(
                    practice_datetime=practice_dt,
                    num_postural_errors=practice.num_postural_errors,
                    num_musical_errors=practice.num_musical_errors,
                    duration=practice.duration,
                    bpm=practice.bpm,
                    figure=practice.figure,
                    octaves=practice.octaves,
                    total_notes_played=practice.total_notes_played,
                    id_student=practice.id_student,
                    id_scale=practice.id_scale,
                )
                session.add(model)
                await session.commit()
                await session.refresh(model)

                logger.info(f"Practice created with id={model.id}")
                return self._model_to_entity(model)

            except IntegrityError as e:
                await session.rollback()
                logger.error(f"Integrity error creating practice: {e}", exc_info=True)
                raise DatabaseConnectionException(f"Integrity error: {str(e)}")

            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"MySQL error creating practice: {e}", exc_info=True)
                raise DatabaseConnectionException(f"Error creating practice: {str(e)}")
            
    async def get_by_datetime_uid_scale(self, datetime: datetime, uid: int, id_scale: int) -> Practice | None:
        async with mysql_connection.get_async_session() as session:
            try:
                stmt = (
                    select(PracticeModel)
                    .where(
                        PracticeModel.practice_datetime == datetime,
                        PracticeModel.id_student == uid,
                        PracticeModel.id_scale == id_scale,
                    )
                )

                result = await session.execute(stmt)
                model = result.scalar_one_or_none()
                if model:
                    return self._model_to_entity(model)
                return None

            except SQLAlchemyError as e:
                logger.error(f"MySQL error fetching practice: {e}", exc_info=True)
                raise DatabaseConnectionException(f"Error fetching practice: {str(e)}")

    
    def _model_to_entity(self, model: PracticeModel) -> Practice:
        dt = model.practice_datetime
        return Practice(
            date=dt.strftime("%Y-%m-%d"),
            time=dt.strftime("%H:%M:%S"),
            scale="",       # DTO
            scale_type="",  # DTO
            num_postural_errors=int(model.num_postural_errors) if model.num_postural_errors else 0,
            num_musical_errors=int(model.num_musical_errors) if model.num_musical_errors else 0,
            duration=int(model.duration) if model.duration else 0,
            bpm=model.bpm,
            figure=model.figure,
            octaves=model.octaves,
            total_notes_played=model.total_notes_played,
            id_student=model.id_student,
            id_scale=model.id_scale,
            id=model.id,
        )