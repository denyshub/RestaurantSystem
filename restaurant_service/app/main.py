from fastapi import FastAPI
from app.routers import restaurant
from app.database import Base, engine
import asyncio

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await init_db()

app.include_router(restaurant.router, prefix="/api/restaurants", tags=["Restaurants"])
