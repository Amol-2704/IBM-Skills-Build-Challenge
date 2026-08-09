from fastapi import FastAPI

from app.api.investigation import router as investigation_router


app = FastAPI(
    title="NEXUS Mission Intelligence API",
    version="0.1.0",
)


app.include_router(investigation_router)


@app.get("/")
def root():
    return {
        "name": "NEXUS",
        "status": "operational",
    }