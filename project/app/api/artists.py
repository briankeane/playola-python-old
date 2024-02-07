from app.config import Settings, get_settings
from app.models.tortoise import Artist
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from spotipy import oauth2
from starlette import status

router = APIRouter()

scopes = ",".join(
    [
        "playlist-read-collaborative",
        "user-follow-read",
        "user-read-playback-position",
        "user-top-read",
        "user-read-recently-played",
        "user-library-read",
        "user-read-email",
        "user-read-currently-playing",
        "user-modify-playback-state",
        "user-read-playback-state",
    ]
)


@router.get("/v1/artists")
async def getArtists(settings: Settings = Depends(get_settings)):
    return await Artist.all()
