from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import readings as readings_repo
from app.schemas.reading import ReadingCreate, ReadingOut


async def ingest(session: AsyncSession, data: ReadingCreate) -> ReadingOut:
    reading = await readings_repo.insert(session, data)
    return ReadingOut.model_validate(reading)