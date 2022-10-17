from fastapi import FastAPI
import databases
import sqlalchemy
import aioredis
import os
from dotenv import load_dotenv
from app.config import POSTGRES_URL, REDIS_URL
app = FastAPI()

basedir = os.path.abspath(os.path.dirname("../"))
load_dotenv(dotenv_path=f"{basedir}/.env")
POSTGRES_URL = os.getenv("POSTGRES_URL")
REDIS_URL = os.getenv("REDIS_URL")
db = databases.Database(POSTGRES_URL)

@app.get("/")
async def root():
    return{"status": "Working"}

@app.on_event("startup")
async def startup():
    await db.connect()
    app.state.redis = await aioredis.from_url(REDIS_URL)

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
    await app.state.redis.close()

