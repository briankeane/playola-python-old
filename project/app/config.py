import logging
from functools import lru_cache

from pydantic import AnyUrl
from pydantic_settings import BaseSettings

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = "dev"
    testing: bool = bool(0)
    database_url: AnyUrl = None
    spotify_client_id: str = "SPOTIFY_CLIENT_ID"
    spotify_client_secret: str = "SPOTIFY_CLIENT_SECRET"
    spotify_redirect_uri: str = "http://localhost:8004/v1/auth/spotify/code"


@lru_cache
def get_settings() -> BaseSettings:
    log.info("loading config settings from the environment...")
    return Settings()
