from app.config import Settings, get_settings
from app.lib.curator import get_or_create_curator
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
        f"{settings.client_base_url}/v1/auth/spotify/code",
        scope=scopes,
        cache_path=".spotipyoauthcache",
    )
    response = sp_oauth.get_access_token(code)
    print(f"client_base_url {settings.client_base_url}")
    return RedirectResponse(
        f"{settings.client_base_url}/curatorSignedIn", status_code=status.HTTP_302_FOUND
    )
    return await get_or_create_curator(token_info=response)


@router.get("/v1/auth/spotify/authorize")
async def spotifyAuthRedirect(settings: Settings = Depends(get_settings)):
    sp_oauth = oauth2.SpotifyOAuth(
        settings.spotify_client_id,
        settings.spotify_client_secret,
        f"{settings.base_url}/v1/auth/spotify/code",
        scope=scopes,
        cache_path=".spotipyoauthcache",
    )

    return RedirectResponse(
        sp_oauth.get_authorize_url(), status_code=status.HTTP_302_FOUND
    )
