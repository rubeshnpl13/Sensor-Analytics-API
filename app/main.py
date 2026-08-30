from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI

from app.api.v1.readings import router as readings_router
from app.core.config import get_settings
from app.core.db import create_engine_and_session_factory, create_tables
from app.core.logging import configure_logging

logger = structlog.get_logger()


def create_app() -> FastAPI:
    """Application factory: builds and configures the FastAPI instance."""
    settings = get_settings()
    configure_logging(settings.log_level, json_logs=settings.environment != "local")

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        engine, session_factory = create_engine_and_session_factory(
            settings.database_url
        )
        app.state.db_engine = engine
        app.state.session_factory = session_factory
        await create_tables(engine)
        logger.info("database_ready")
        yield
        await engine.dispose()
        logger.info("database_engine_stopped")

    app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
    app.include_router(readings_router, prefix="/api/v1")

    @app.get("/health")
    def health() -> dict[str, str]:
        logger.info("health_check", status="ok")
        return {"status": "ok"}

    return app


app = create_app()