import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import curators, healthcheck, spotify_auth
from app.db import init_db

log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(healthcheck.router)
    application.include_router(spotify_auth.router)
    application.include_router(curators.router)

    return application


app = create_application()
origins = ["http://localhost:3000", "https://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
