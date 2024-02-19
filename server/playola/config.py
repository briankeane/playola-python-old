import logging
from functools import lru_cache

from pydantic import AnyUrl
from pydantic_settings import BaseSettings

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = "dev"
    base_url: str = "http://localhost:8004"
    testing: bool = bool(0)
    database_url: AnyUrl = None
    spotify_client_id: str = "SPOTIFY_CLIENT_ID"
    spotify_client_secret: str = "SPOTIFY_CLIENT_SECRET"
    spotify_redirect_uri: str = f"{base_url}/v1/auth/spotify/code"
    client_base_url: str = "http://localhost:3000"


@lru_cache
def get_settings() -> BaseSettings:
    log.info("loading config settings from the environment...")
    return Settings()
