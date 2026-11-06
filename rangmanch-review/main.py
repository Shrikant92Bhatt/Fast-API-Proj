from database import create_db_and_tables
from contextlib import asynccontextmanager
from fastapi import FastAPI
from routes.reviews import router as review_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager - Used to create database tables on startup."""
    create_db_and_tables()
    print("Database tables created successfully")
    yield
    print("Shuting down the application")


app = FastAPI(
    title = "Rangmanch Review API",
    description = "API for managing theatre reviews.",
    version = "1.0.0",
    lifespan=lifespan
)

app.include_router(review_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Rangmanch Review API"}

