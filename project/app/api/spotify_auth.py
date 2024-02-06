from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from starlette import status
from app.config import Settings, get_settings
from spotipy import oauth2

router = APIRouter()

@router.get("/v1/auth/spotify/code")
def spotifyAuthCode(code: str, settings: Settings = Depends(get_settings)):
    sp_oauth = oauth2.SpotifyOAuth(settings.spotify_client_id, settings.spotify_client_secret, "http://localhost:8004/v1/auth/spotify/code", scope='user-library-read', cache_path='.spotipyoauthcache')
    token_info = sp_oauth.get_access_token(code)
    return { "token" : token_info["access_token"] }


@router.get("/v1/auth/spotify/authorize")
async def spotifyAuthRedirect(settings: Settings = Depends(get_settings), redirect_uri: str = "http://thisisatest"):
    sp_oauth = oauth2.SpotifyOAuth(settings.spotify_client_id, settings.spotify_client_secret, "http://localhost:8004/v1/auth/spotify/code", scope='user-library-read', cache_path='.spotipyoauthcache')
    
    return RedirectResponse(sp_oauth.get_authorize_url(), status_code=status.HTTP_302_FOUND)
