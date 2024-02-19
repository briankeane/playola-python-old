import json

from tortoise import Tortoise, fields, models
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator


class CuratorTrackStatus:
    approved = "approved"
    denied = "denied"
    new = "new"


class Curator(models.Model):
    spotify_token_info = fields.JSONField()
    spotify_user_id = fields.CharField(max_length=512)
    spotify_display_name = fields.CharField(max_length=512)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} -- {self.spotify_user_id}"


class Track(models.Model):
    spotify_id = fields.CharField(max_length=512, unique=True)
    album = fields.CharField(max_length=512)
    artist = fields.CharField(max_length=512)
    duration_ms = fields.IntField()
    isrc = fields.CharField(max_length=512)
    title = fields.CharField(max_length=512)
    popularity = fields.IntField()
    spotify_image_link = fields.CharField(max_length=512)


class CuratorTrack(models.Model):
    curator = fields.ForeignKeyField("models.Curator", related_name="curator_tracks")
    track = fields.ForeignKeyField("models.Track", related_name="curator_tracks")
    status = fields.CharField(max_length=512)


Tortoise.init_models(["playola.models.tortoise"], "models")

CuratorTrack_Pydantic = pydantic_model_creator(CuratorTrack)
print(json.dumps(CuratorTrack_Pydantic.schema(), indent=4))
CuratorTrack_Pydantic_List = pydantic_queryset_creator(CuratorTrack)
