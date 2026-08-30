import structlog
from fastapi import FastAPI

from app.core.config import get_settings
from app.core.logging import configure_logging
from app.api.v1.readings import router as readings_router

logger = structlog.get_logger()


def create_app() -> FastAPI:
    """Application factory: builds and configures the FastAPI instance."""
    settings = get_settings()
    configure_logging(
        settings.log_level,
        json_logs=settings.environment != "local",
    )

    app = FastAPI(title=settings.app_name, version="0.1.0")
    app = FastAPI(title=settings.app_name, version="0.1.0")
    app.include_router(readings_router, prefix="/api/v1")
    
    @app.get("/health")
    def health() -> dict[str, str]:
        logger.info("health_check", status="ok")
        return {"status": "ok"}

    return app


app = create_app()
