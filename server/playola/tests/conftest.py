import os
from typing import AsyncGenerator, Generator
from unittest.mock import AsyncMock, Mock

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, Request, Response

os.environ["ENV_STATE"] = "test"
from playola.database import database, user_table, curator_table  # noqa: E402
from playola.main import app  # noqa: E402


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture()
def client() -> Generator:
    yield TestClient(app)


@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    await database.connect()
    yield
    await database.disconnect()


@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        yield ac


@pytest.fixture()
async def registered_user(async_client: AsyncClient) -> dict:
    user_details = {"email": "test@example.net", "password": "1234"}
    await async_client.post("/register", json=user_details)
    query = user_table.select().where(user_table.c.email == user_details["email"])
    user = await database.fetch_one(query)
    user_details["id"] = user.id
    return user_details

@pytest.fixture()
async def created_curator(async_client: AsyncClient) -> dict:
    curator_details = {"spotify_user_id": "lonesomewhistle", 
                       "spotify_token_info": {
                           "access_token": "this_is_an_access_token", 
                           "token_type": "Bearer", 
                           "expires_in": 3600, 
                           "scope": "playlist-read-collaborative user-follow-read user-library-read user-modify-playback-state user-read-currently-playing user-read-email user-read-playback-position user-read-playback-state user-read-recently-played user-top-read", 
                           "expires_at": 1708196856, 
                           "refresh_token": "this_is_a_refresh_token"
                        },
                        "spotify_display_name": "Brian Keane"
                    }
    query = curator_table.insert(values=curator_details)
    inserted_id = await database.execute(query)
    curator_details["id"] = inserted_id
    return curator_details
    

@pytest.fixture()
async def confirmed_user(registered_user: dict) -> dict:
    query = (
        user_table.update()
        .where(user_table.c.email == registered_user["email"])
        .values(confirmed=True)
    )
    await database.execute(query)
    return registered_user


@pytest.fixture()
async def logged_in_token(async_client: AsyncClient, confirmed_user: dict) -> str:
    response = await async_client.post("/token", json=confirmed_user)
    return response.json()["access_token"]


@pytest.fixture(autouse=True)
def mock_httpx_client(mocker):
    """
    Fixture to mock the HTTPX client so that we never make any
    real HTTP requests (especially important when registering users).
    """
    mocked_client = mocker.patch("playola.tasks.httpx.AsyncClient")

    mocked_async_client = Mock()
    response = Response(status_code=200, content="", request=Request("POST", "//"))
    mocked_async_client.post = AsyncMock(return_value=response)
    mocked_client.return_value.__aenter__.return_value = mocked_async_client

    return mocked_async_client
