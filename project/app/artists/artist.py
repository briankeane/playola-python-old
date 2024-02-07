import spotipy

from app.models.tortoise import Artist


async def create_artist(access_token: str):
    sp = spotipy.Spotify(auth=access_token)
    user = sp.current_user()
    artist = await Artist.filter(spotify_id=user["id"]).first()
    if artist is None:
        artist = await Artist.create(
            spotify_access_token=access_token,
            spotify_id=user["id"],
            spotify_display_name=user["display_name"],
        )
    return artist
