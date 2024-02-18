from tortoise import fields, models


class Curator(models.Model):
    spotify_token_info = fields.JSONField()
    spotify_user_id = fields.CharField(max_length=512)
    spotify_display_name = fields.CharField(max_length=512)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} -- {self.spotify_user_id}"


class Track(models.Model):
    spotify_id = fields.CharField(max_length=512)
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
    approved = fields.BooleanField(null=True)
    date_last_seen = fields.DateField()
