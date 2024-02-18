import datetime
import json
from typing import Optional

import spotipy
from app.lib.errors import ItemNotFoundException
from app.lib.spotipy_extensions import UserSpecificSpotify
from app.models.tortoise import Curator, CuratorTrack, Track


async def get_or_create_curator(token_info: dict) -> Curator:
    sp = spotipy.Spotify(auth=token_info["access_token"])
    user = sp.current_user()
    (curator, created) = await Curator.get_or_create(
        spotify_user_id=user["id"],
        defaults={
            "spotify_token_info": token_info,
            "spotify_display_name": user["display_name"],
        },
    )
    print("curator: ", curator)
    return curator


async def refresh_curators_important_tracks(curator_id: str):
    curator = await Curator.filter(id=curator_id).first()
    if curator is None:
        raise ItemNotFoundException

    sp = UserSpecificSpotify(curator=curator)
    track_infos_short_term = sp.current_user_top_tracks(
        limit=50, time_range="short_term"
    )["items"]
    track_infos_medium_term = sp.current_user_top_tracks(
        limit=50, time_range="medium_term"
    )["items"]
    track_infos_long_term = sp.current_user_top_tracks(
        limit=50, time_range="long_term"
    )["items"]

    all_track_infos = remove_duplicates(
        track_infos_short_term + track_infos_medium_term + track_infos_long_term
    )

    tracks = []

    for track_info in all_track_infos:
        (track, created) = await Track.get_or_create(
            spotify_id=track_info["id"],
            defaults={
                "album": parse_album(track_info),
                "artist": parse_artist(track_info),
                "duration_ms": track_info["duration_ms"],
                "isrc": parse_isrc(track_info),
                "title": track_info["name"],
                "popularity": track_info["popularity"],
                "spotify_image_link": parse_spotify_image_link(track_info),
            },
        )
        tracks.append(track)

    curator_tracks = []
    for track in tracks:
        (track, created) = await CuratorTrack.get_or_create(
            curator_id=curator.id,
            track_id=track.id,
            defaults={"date_last_seen": datetime.datetime.now()},
        )
        curator_tracks.append(await track.fetch_related("curator", "track"))

    return curator_tracks


def parse_album(track_info) -> str:
    return track_info["album"]["name"]


def parse_artist(track_info) -> Optional[str]:
    return track_info["artists"][0]["name"]


def parse_isrc(track_info) -> Optional[str]:
    return track_info.get("external_ids", {}).get("isrc", None)


def parse_spotify_image_link(track_info) -> Optional[str]:
    images = track_info["album"]["images"]
    if not len(images):
        return None
    return images[0]


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
