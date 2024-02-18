import pytest
from httpx import AsyncClient

from playola import security

from playola.models.curator import Curator


@pytest.fixture()
async def created_curator_track(async_client: AsyncClient, created_curator):
    return await create_post("Test Post", async_client, logged_in_token)
