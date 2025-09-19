import logging
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.core.exceptions import DatabaseConnectionException
from app.domain.entities.scale import Scale
from app.domain.repositories.i_scale_repo import IScaleRepo
from app.infrastructure.database.models.scale_model import ScaleModel
from app.infrastructure.database.mysql_connection import mysql_connection

logger = logging.getLogger(__name__)

class MySQLScaleRepository(IScaleRepo):
    """Concrete implementation of IScaleRepo for Scale using MySQL."""

    async def create(self, scale: Scale) -> Scale:
        async with mysql_connection.get_async_session() as session:
            try:
                model = ScaleModel(
                    name=scale.name,
                    scale_type=scale.scale_type,
                )
                session.add(model)
                await session.commit()
                await session.refresh(model)

                logger.info(f"Scale created with id={model.id}")
                return self._model_to_entity(model)

            except IntegrityError as e:
                await session.rollback()
                logger.error(f"Integrity error creating scale: {e}", exc_info=True)
                raise DatabaseConnectionException(f"Integrity error: {str(e)}")

            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"MySQL error creating scale: {e}", exc_info=True)
                raise DatabaseConnectionException(f"Error creating scale: {str(e)}")

    async def get_by_name_and_type(self, name: str, scale_type: str) -> Scale | None:
        async with mysql_connection.get_async_session() as session:
            try:
                stmt = select(ScaleModel).where(
                    ScaleModel.name == name,
                    ScaleModel.scale_type == scale_type,
                )
                result = await session.execute(stmt)
                model = result.scalar_one_or_none()
                if model:
                    return self._model_to_entity(model)
                return None

            except SQLAlchemyError as e:
                logger.error(f"MySQL error fetching scale: {e}", exc_info=True)
                raise DatabaseConnectionException(f"Error fetching scale: {str(e)}")

    def _model_to_entity(self, model: ScaleModel) -> Scale:
        return Scale(
            name=model.name,
            scale_type=model.scale_type,
            id=model.id,
        )
