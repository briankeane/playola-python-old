import databases
import sqlalchemy
import json
import pydantic

from playola.config import config

class CuratorTrackStatus:
    accepted = "ACCEPTED"
    rejected = "REJECTED"
    new = "NEW"
    deleted = "DELETED"


metadata = sqlalchemy.MetaData()

post_table = sqlalchemy.Table(
    "posts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("body", sqlalchemy.String),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id"), nullable=False),
    sqlalchemy.Column("image_url", sqlalchemy.String),
)

user_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("confirmed", sqlalchemy.Boolean, default=False)
)


comment_table = sqlalchemy.Table(
    "comments",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("body", sqlalchemy.String),
    sqlalchemy.Column("post_id", sqlalchemy.ForeignKey("posts.id"), nullable=False),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id"), nullable=False)
)

like_table = sqlalchemy.Table(
    "likes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("post_id", sqlalchemy.ForeignKey("posts.id"), nullable=False),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id"), nullable=False)
)

curator_table = sqlalchemy.Table(
    "curators",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("spotify_user_id", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("spotify_token_info", sqlalchemy.JSON, nullable=False),
    sqlalchemy.Column("spotify_display_name", sqlalchemy.String, unique=True, nullable=False),
)

track_table = sqlalchemy.Table(
    "tracks",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("spotify_id", sqlalchemy.String, unique=True, nullable=False),
    sqlalchemy.Column("title", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("album", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("duration_ms", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("isrc", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("popularity", sqlalchemy.Integer, nullable=True),
    sqlalchemy.Column("spotify_image_link", sqlalchemy.String, nullable=True)
)

curator_track_table = sqlalchemy.Table(
    "curator_tracks",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("curator_id", sqlalchemy.ForeignKey("curators.id"), nullable=False),
    sqlalchemy.Column("track_id", sqlalchemy.ForeignKey("tracks.id"), nullable=False),
    sqlalchemy.Column("status", sqlalchemy.String, default="new"),
    sqlalchemy.Column("date_of_status_change", sqlalchemy.Date, nullable=True),
)

def _custom_json_serializer(*args, **kwargs) -> str:
    """
    Encodes json in the same way that pydantic does.
    """
    return json.dumps(*args, default=pydantic.json.pydantic_encoder, **kwargs)

engine = sqlalchemy.create_engine(
    config.DATABASE_URL, json_serializer=_custom_json_serializer
)

metadata.create_all(engine)
database = databases.Database(
    config.DATABASE_URL, force_rollback=config.DB_FORCE_ROLL_BACK
)
