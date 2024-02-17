import json

import pytest
from app.lib.curator import get_curators_important_tracks, remove_duplicates
from app.lib.spotipy_extensions import UserSpecificSpotify
from app.models.tortoise import Curator


def load_track_response(time_range: str):
    f = open(f"app/lib/tests/spotify_responses/users_top_tracks_{time_range}_term.json")
    data = json.load(f)
    f.close()
    return data


class MockSpotify:
    def current_user_top_tracks(limit: int, time_range: str):
        return load_track_response(time_range)


def test_remove_duplicates():
    long_tracks = load_track_response("long")["items"]
    medium_tracks = load_track_response("medium")["items"]
    short_tracks = load_track_response("short")["items"]

    tracks_list = remove_duplicates(long_tracks + medium_tracks + short_tracks)
    assert len(tracks_list) == 13
    ids = list(map(lambda x: x["id"], tracks_list))
    assert len(ids) == len(set(ids))


@pytest.mark.anyio
async def test_get_curators_important_tracks(mocker):
    curator = await Curator.create(
        spotify_token_info={},
        spotify_user_id="spotify_user_id",
        spotify_display_name="spotify_display_name",
    )
    mocker.patch(
        "app.lib.spotipy_extensions.UserSpecificSpotify",
        return_value=MockSpotify(),
    )
    tracks = get_curators_important_tracks(curator_id=curator.id)
    print(tracks)
