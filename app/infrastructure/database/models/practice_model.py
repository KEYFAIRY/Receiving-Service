from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.infrastructure.database.models.base import Base

class PracticeModel(Base):
    __tablename__ = "Practice"

    id = Column(Integer, primary_key=True, autoincrement=True)
    practice_datetime = Column(DateTime, nullable=False)
    num_postural_errors = Column(Numeric, nullable=True)
    num_musical_errors = Column(Numeric, nullable=True)
    duration = Column(Numeric, nullable=False)
    bpm = Column(Integer, nullable=False)
    id_student = Column(String(128), nullable=False)

    id_scale = Column(Integer, ForeignKey("Scale.id"), nullable=False)

    scale = relationship("ScaleModel", back_populates="practices")
