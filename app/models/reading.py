from datetime import datetime

from sqlalchemy import DateTime, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Reading(Base):
    __tablename__ = "readings"

    id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[str] = mapped_column(String(100))
    metric: Mapped[str] = mapped_column(String(50))
    value: Mapped[float]
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        Index("ix_readings_device_timestamp", "device_id", "timestamp"),
    )