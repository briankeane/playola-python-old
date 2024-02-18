# Most of this taken from Redowan Delowar's post on configurations with Pydantic
# https://rednafi.github.io/digressions/python/2020/06/03/python-configs.html
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    ENVIRONMENT: Optional[str] = None

    """Loads the dotenv file. Including this is necessary to get
    pydantic to load a .env file."""
    model_config = SettingsConfigDict(env_file=".env")


class GlobalConfig(BaseConfig):
    DATABASE_URL: Optional[str] = None
    DB_FORCE_ROLL_BACK: bool = False
    MAILGUN_DOMAIN: Optional[str] = None
    MAILGUN_API_KEY: Optional[str] = None
    LOGTAIL_API_KEY: Optional[str] = None
    B2_KEY_ID: Optional[str] = None
    B2_APPLICATION_KEY: Optional[str] = None
    B2_BUCKET_NAME: Optional[str] = None
    DEEPAI_API_KEY: Optional[str] = None
    SPOTIFY_CLIENT_ID: str = "SPOTIFY_CLIENT_ID"
    SPOTIFY_CLIENT_SECRET: str = "SPOTIFY_CLIENT_SECRET"
    BASE_URL: str = "http://localhost:8004"
    CLIENT_BASE_URL: str = "http://localhost:3000"
    SPOTIFY_REDIRECT_URI: str = f"{BASE_URL}/v1/auth/spotify/code"


class DevConfig(GlobalConfig):
    pass
    # model_config = SettingsConfigDict(env_prefix="DEV_")


class ProdConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="PROD_")


class TestConfig(GlobalConfig):
    DATABASE_URL: str = "sqlite:///test.db"
    DB_FORCE_ROLL_BACK: bool = True

    model_config = SettingsConfigDict(env_prefix="TEST_")


@lru_cache()
def get_config(environment: str):
    """Instantiate config based on the environment."""
    configs = {"dev": DevConfig, "prod": ProdConfig, "test": TestConfig}
    return configs[environment]()


config = get_config(BaseConfig().ENVIRONMENT)
