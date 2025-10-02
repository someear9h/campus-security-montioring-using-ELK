import uvicorn
from fastapi import FastAPI
from routers.card_swipes import router as card_swipes_router
from routers.entity import router as entity_router

# Initialize FastAPI
app = FastAPI(
    title="Campus Security Monitoring API",
    description="An API to ingest and query campus card swipe data in real-time.",
    version="1.0.0"
)

# Include routers
app.include_router(card_swipes_router, prefix="/card-swipes", tags=["Card Swipes"])
app.include_router(entity_router, prefix="/entity", tags=["Entity Resolution"])

@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "Welcome to the Campus Security API.",
        "docs_url": "/docs"
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
