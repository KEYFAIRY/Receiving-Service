from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from app.infrastructure.database.models.base import Base

class ScaleModel(Base):
    __tablename__ = "Scale"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    scale_type = Column(String(50), nullable=False)

    practices = relationship("PracticeModel", back_populates="scale")

    __table_args__ = (
        UniqueConstraint("name", "scale_type", name="uq_scale"),
    )
