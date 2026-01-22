from fastapi import FastAPI

app = FastAPI(title="Legalmind API")


@app.get("/health")
def health_check() -> dict[str, str]:
    """Simple liveness probe."""
    return {"status": "ok"}
