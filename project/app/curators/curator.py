import spotipy
from app.models.tortoise import Curator
from app.spotipy_extensions import UserSpecificSpotify


class CuratorNotFoundException(Exception):
    pass


async def create_curator(token_info: dict):
    sp = spotipy.Spotify(auth=token_info["access_token"])
    user = sp.current_user()
    curator = await Curator.filter(spotify_user_id=user["id"]).first()
    if curator is None:
        curator = await Curator.create(
            spotify_token_info=token_info,
            spotify_user_id=user["id"],
            spotify_display_name=user["display_name"],
        )

    sp2 = await UserSpecificSpotify(spotify_user_id=curator.spotify_user_id)
    tracks = sp2.current_user_top_tracks(limit=50, time_range="short_term")
    print(tracks)

    return curator


async def get_curators_short_term_songs(curator_id: str):
    curator = await Curator.filter(id=curator_id).first()
    if curator is None:
        raise CuratorNotFoundException

    sp = await UserSpecificSpotify(spotify_user_id=curator.spotify_user_id)
    tracks = sp.current_user_top_tracks(limit=50, time_range="short_term")
    print(tracks)
    return tracks
