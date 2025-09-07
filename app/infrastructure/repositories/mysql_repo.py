import logging
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.core.exceptions import DatabaseConnectionException
from app.domain.entities.practice import Practice
from app.domain.repositories.i_mysql_repo import IMySQLRepo
from app.infrastructure.database.models.practice_model import PracticeModel
from app.infrastructure.database.mysql_connection import mysql_connection

logger = logging.getLogger(__name__)


class MySQLPracticeRepository(IMySQLRepo):
    """Concrete implementation of IMySQLRepo for Practice using MySQL."""

    async def create(self, practice: Practice) -> Practice:
        async with mysql_connection.get_async_session() as session:
            try:
                model = PracticeModel(
                    date=practice.date,
                    time=practice.time,
                    num_postural_errors=practice.num_postural_errors,
                    num_musical_errors=practice.num_musical_errors,
                    duration=practice.duration,
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

    def _model_to_entity(self, model: PracticeModel) -> Practice:
        return Practice(
            id=model.id,
            date=model.date,
            time=model.time,
            num_postural_errors=model.num_postural_errors,
            num_musical_errors=model.num_musical_errors,
            duration=model.duration,
            id_student=model.id_student,
            id_scale=model.id_scale,
        )
