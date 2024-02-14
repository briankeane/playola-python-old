import json

import spotipy
from app.lib.errors import ItemNotFoundException
from app.lib.spotipy_extensions import UserSpecificSpotify
from app.models.tortoise import Curator


async def get_or_create_curator(token_info: dict):
    sp = spotipy.Spotify(auth=token_info["access_token"])
    user = sp.current_user()
    curator = await Curator.filter(spotify_user_id=user["id"]).first()
    if curator is None:
        curator = await Curator.create(
            spotify_token_info=token_info,
            spotify_user_id=user["id"],
            spotify_display_name=user["display_name"],
        )
    return curator


async def get_curators_important_tracks(curator_id: str):
    curator = await Curator.filter(id=curator_id).first()
    if curator is None:
        raise ItemNotFoundException

    sp = UserSpecificSpotify(curator=curator)
    tracks_short_term = sp.current_user_top_tracks(limit=50, time_range="short_term")[
        "items"
    ]
    tracks_medium_term = sp.current_user_top_tracks(limit=50, time_range="medium_term")[
        "items"
    ]
    tracks_long_term = sp.current_user_top_tracks(limit=50, time_range="long_term")[
        "items"
    ]

    return remove_duplicates(tracks_short_term + tracks_medium_term + tracks_long_term)


def remove_duplicates(tracks_list: list):
    tracks_dict = {}
    final_list = []
    for track in tracks_list:
        if tracks_dict.get(track["id"]) is None:
            tracks_dict[track["id"]] = True
            final_list.append(track)
    return final_list


async def get_all_curators():
    return await Curator.all()


async def get_curator(id):
    curator = await Curator.filter(id=id).first()
    if curator is None:
        raise ItemNotFoundException
    return curator
    curator = await Curator.filter(id=id).first()
    if curator is None:
        raise ItemNotFoundException
    return curator
    return curator
    return curator
    return curator
