from fastapi import FastAPI


def create_app() -> FastAPI:
    """Application factory: builds and configures the FastAPI instance."""
    app = FastAPI(title="Sensor Analytics API", version="0.1.0")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()