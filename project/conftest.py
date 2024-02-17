import os

import pytest
from app.config import Settings, get_settings
from app.main import app
from httpx import AsyncClient
from starlette.testclient import TestClient
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.test import finalizer, initializer


def get_settings_override():
    return Settings(testing=1, database_url=os.environ.get("DATABASE_TEST_URL"))


async def init_db(db_url, create_db: bool = False, schemas: bool = False) -> None:
    """Initial database connection"""
    await Tortoise.init(
        db_url=db_url,
        modules={"models": ["models"]},
        _create_db=create_db,
    )
    if create_db:
        print(f"Database created! {db_url = }")
    if schemas:
        await Tortoise.generate_schemas()
        print("Success to generate schemas")


async def init(db_url: str = os.environ.get("DATABASE_TEST_URL")):
    print("------------------- here ------------------")
    print(db_url)
    await init_db(db_url, True, True)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        print("Client is ready")
        yield client


@pytest.fixture(scope="session", autouse=True)
async def initialize_tests():
    print("---------------------------------------")
    await init()
    yield
    await Tortoise._drop_databases()


@pytest.fixture(scope="module")
def test_app():
    # set up
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:
        # testing
        yield test_client

    # tear down
