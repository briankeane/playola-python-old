from app.config import get_settings
from app.models.tortoise import Curator
from spotipy import CacheHandler, Spotify, SpotifyOAuth


class UserSpecificCacheHandler(CacheHandler):
    def __init__(self, curator):
        self.curator = curator

    def get_cached_token(self):
        print("getting cached info", self.curator.spotify_token_info)
        return self.curator.spotify_token_info

    def save_token_to_cache(self, token_info):
        print("saving token info: ", token_info)
        self.curator.spotify_token_info = token_info
        self.curator.save()


async def create_user_specific_spotify(spotify_user_id):
    curator = await Curator.filter(spotify_user_id=spotify_user_id).first()
    cache_handler = UserSpecificCacheHandler(curator=curator)
    settings = get_settings()

    return SpotifyOAuth(
        client_id=settings.spotify_client_id,
        client_secret=settings.spotify_client_secret,
        redirect_uri="http://localhost:8004/v1/auth/spotify/code",
        cache_handler=cache_handler,
    )


class UserSpecificSpotify(Spotify):
    def __init__(self, cache_handler):
        self.cache_handler = cache_handler
        super().__init__()
