import logging

from playola.config import config

from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from spotipy import oauth2
from starlette import status

import spotipy

logging = logging.getLogger(__name__)
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

def get_or_create_curator(token_info):
    sp = spotipy.Spotify(auth=token_info["access_token"])
    user = sp.current_user()



@router.get("/v1/auth/spotify/code")
async def spotifyAuthCode(code: str):
    sp_oauth = oauth2.SpotifyOAuth(
        config.SPOTIFY_CLIENT_ID,
        config.SPOTIFY_CLIENT_SECRET,
        f"{config.BASE_URL}/v1/auth/spotify/code",
        scope=scopes,
        cache_path=".spotipyoauthcache",
    )
    response = sp_oauth.get_access_token(code)
    curator = await get_or_create_curator(token_info=response)
    return RedirectResponse(
        f"{config.CLIENT_BASE_URL}/curators/{curator.id}",
        status_code=status.HTTP_302_FOUND,
    )


@router.get("/v1/auth/spotify/authorize")
async def spotifyAuthRedirect():
    sp_oauth = oauth2.SpotifyOAuth(
        config.SPOTIFY_CLIENT_ID,
        config.SPOTIFY_CLIENT_SECRET,
        f"{config.BASE_URL}/v1/auth/spotify/code",
        scope=scopes,
        cache_path=".spotipyoauthcache",
    )

    return RedirectResponse(
        sp_oauth.get_authorize_url(), status_code=status.HTTP_302_FOUND
    )
