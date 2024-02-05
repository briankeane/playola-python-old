from tortoise import fields, models


class Client(models.Model):
    client_id = fields.UUIDField()
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.id
