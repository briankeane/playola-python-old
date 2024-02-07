from tortoise import fields, models


class Artist(models.Model):
    spotify_access_token = fields.CharField(max_length=512)
    spotify_id = fields.CharField(max_length=512)
    spotify_display_name = fields.CharField(max_length=512)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.id
