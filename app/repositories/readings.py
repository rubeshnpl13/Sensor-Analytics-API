from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Reading
from app.schemas.reading import ReadingCreate


async def insert(session: AsyncSession, data: ReadingCreate) -> Reading:
    reading = Reading(
        device_id=data.device_id,
        metric=data.metric.value,
        value=data.value,
        timestamp=data.timestamp,
    )
    session.add(reading)
    await session.commit()
    await session.refresh(reading)
    return reading