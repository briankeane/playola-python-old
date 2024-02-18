import logging
import os

from fastapi import FastAPI
from tortoise import Tortoise, run_async
from tortoise.contrib.fastapi import register_tortoise

log = logging.getLogger("uvicorn")


TORTOISE_ORM = {
    "connections": {"default": os.environ.get("DATABASE_URL")},
    "playolas": {
        "models": {
            "models": ["playola.models.tortoise", "aerich.models"],
            "default_connection": "default",
        },
    },
}


def init_db(playola: FastAPI) -> None:
    register_tortoise(
        playola,
        db_url=os.environ.get("DATABASE_URL"),
        modules={"models": ["playola.models.tortoise"]},
        generate_schemas=False,
        add_exception_handlers=True,
    )


async def generate_schema() -> None:
    log.info("Initializing Tortoise...")

    await Tortoise.init(
        db_url=os.environ.get("DATABASE_URL"),
        modules={"models": ["models.tortoise"]},
    )
    log.info("Generating database schema via Tortoise...")
    await Tortoise.generate_schemas()
    await Tortoise.close_connections()


if __name__ == "__main__":
    run_async(generate_schema())
