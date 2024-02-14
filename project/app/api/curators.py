from app.config import Settings, get_settings
from app.lib.curator import get_all_curators, get_curator, get_curators_important_tracks
from app.lib.errors import ItemNotFoundException
from app.lib.spotipy_extensions import UserSpecificSpotify
from app.models.tortoise import Curator
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from spotipy import Spotify, oauth2
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


@router.get("/v1/curators")
async def getCurators(settings: Settings = Depends(get_settings)):
    return await get_all_curators()


@router.get("/v1/curators/{curator_id}")
async def getCurator(curator_id: str, settings: Settings = Depends(get_settings)):
    try:
        curator = get_curator(id=curator_id)
    except ItemNotFoundException:
        raise HTTPException(status_code=404, detail="Curator not found")
    return curator


@router.get("/v1/curators/{curator_id}/importantTracks")
async def getCuratorsImportantTracks(
    curator_id: str, settings: Settings = Depends(get_settings)
):
    try:
        return await get_curators_important_tracks(curator_id=curator_id)
    except ItemNotFoundException:
        return HTTPException(status_code=404, detail="Curator not found")
