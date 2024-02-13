from app.config import Settings, get_settings
from app.curators.curator import get_curators_short_term_songs
from app.models.tortoise import Curator
from app.spotipy_extensions import UserSpecificSpotify, create_user_specific_spotify
from fastapi import APIRouter, Depends
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
    return await Curator.all()


@router.get("/v1/curators/{curator_id}")
async def getCurator(curator_id: str, settings: Settings = Depends(get_settings)):
    curator = await Curator.filter(id=curator_id).first()

    sp_oath_manager = await create_user_specific_spotify(
        spotify_user_id=curator.spotify_user_id
    )
    sp = Spotify(oauth_manager=sp_oath_manager)
    # print(sp.oauth_manager.cache_handler.curator)
    return sp.current_user_top_tracks(time_range="long_term")
    return curator


@router.get("/v1/curators/{artist_id}/shortTermTracks")
async def getShortTermTracks(
    artist_id: str, settings: Settings = Depends(get_settings)
):
    return await get_artist_short_term_songs(artist_id=artist_id)
