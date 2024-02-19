from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from playola.config import Settings, get_settings
from playola.lib.curator import (
    get_all_curators,
    get_curator,
    refresh_curators_important_tracks,
)
from playola.lib.errors import ItemNotFoundException
from playola.lib.spotipy_extensions import UserSpecificSpotify
from playola.models.tortoise import (
    Curator,
    CuratorTrack,
    CuratorTrack_Pydantic_List,
    Track,
)
from spotipy import Spotify, oauth2

# from playola.models.pydantic import CuratorTrackSchema


router = APIRouter()

scopes = ",".join(
    [
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
    return await CuratorTrack_Pydantic_List.from_queryset(
        CuratorTrack.filter(curator_id=curator_id).select_related("track")
    )
    # return await Track.all()
    return await CuratorTrack.filter(curator_id=curator_id).select_related(
        "track", "curator"
    )
    try:
        return await refresh_curators_important_tracks(curator_id=curator_id)
    except ItemNotFoundException:
        return HTTPException(status_code=404, detail="Curator not found")
