from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from playola.config import Settings, get_settings
from playola.lib.curator import get_or_create_curator
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
        f"{settings.base_url}/v1/auth/spotify/code",
        scope=scopes,
    )
    response = sp_oauth.get_access_token(code, check_cache=False)
    print(f"client_base_url {settings.client_base_url}")
    print("code: ", code)
    print("response: ", response)
    curator = await get_or_create_curator(token_info=response)
    return RedirectResponse(
        f"{settings.client_base_url}/curators/{curator.id}",
        status_code=status.HTTP_302_FOUND,
    )


@router.get("/v1/auth/spotify/authorize")
async def spotifyAuthRedirect(settings: Settings = Depends(get_settings)):
    sp_oauth = oauth2.SpotifyOAuth(
        settings.spotify_client_id,
        settings.spotify_client_secret,
        f"{settings.base_url}/v1/auth/spotify/code",
        scope=scopes,
    )

    return RedirectResponse(
        sp_oauth.get_authorize_url(), status_code=status.HTTP_302_FOUND
    )
