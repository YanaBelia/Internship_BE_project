import os
# from urllib.request import Request

from databases import Database
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.routing import Mount

from app.my_data.database import SQLALCHEMY_DATABASE_URL, engine
from fastapi.middleware.cors import CORSMiddleware

from app.models import models
from app.router.auth import router1

from app.router.routes import router
import databases


async def init_models():
    async with engine.begin() as con:
        await con.run_sync(models.Base.metadata.drop_all)
        await con.run_sync(models.Base.metadata.create_all)

app = FastAPI()
basedir = os.path.abspath(os.path.dirname("../"))
load_dotenv(dotenv_path=f"{basedir}/.env")

db = databases.Database(SQLALCHEMY_DATABASE_URL)
app.include_router(router, prefix="/user", tags=["user"])
app.include_router(router1, prefix="/auth", tags=["auth"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,  # Add CORSMiddleware from BE-3*
    allow_headers=["*"],
    allow_methods=["*"],
)


# @app.get("/")
# async def root():
#     return {"status": "Working"}


def inject_db(app: FastAPI, db: Database):
    app.state.database = db
    for route in app.router.routes:
        if isinstance(route, Mount):
            route.app.state.database = db


@app.on_event("startup")
async def startup():
    await db.connect()
    inject_db(app, db)


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
    # await app.state.redis.close()
