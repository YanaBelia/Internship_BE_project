from fastapi import FastAPI
import databases
import aioredis
import os
from dotenv import load_dotenv
from app.config import POSTGRES_URL, REDIS_URL
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

basedir = os.path.abspath(os.path.dirname("../"))
load_dotenv(dotenv_path=f"{basedir}/.env")

db = databases.Database(POSTGRES_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,                  #Add CORSMiddleware from BE-3*
    allow_headers=["*"],
    allow_methods=["*"],
)
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
