from app.artists.artist import create_artist
from app.config import Settings, get_settings
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


@router.get("/v1/auth/spotify/code")
async def spotifyAuthCode(code: str, settings: Settings = Depends(get_settings)):
    sp_oauth = oauth2.SpotifyOAuth(
        settings.spotify_client_id,
        settings.spotify_client_secret,
        "http://localhost:8004/v1/auth/spotify/code",
        scope=scopes,
        cache_path=".spotipyoauthcache",
    )
    access_token = sp_oauth.get_access_token(code)["access_token"]
    return await create_artist(access_token)


@router.get("/v1/auth/spotify/authorize")
async def spotifyAuthRedirect(
    settings: Settings = Depends(get_settings), redirect_uri: str = "http://thisisatest"
):
    sp_oauth = oauth2.SpotifyOAuth(
        settings.spotify_client_id,
        settings.spotify_client_secret,
        "http://localhost:8004/v1/auth/spotify/code",
        scope=scopes,
        cache_path=".spotipyoauthcache",
    )

    return RedirectResponse(
        sp_oauth.get_authorize_url(), status_code=status.HTTP_302_FOUND
    )
