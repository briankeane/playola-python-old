from pydantic import BaseModel, ConfigDict, json

class Curator(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    id: int
    spotify_user_id: str
    spotify_token_info: json
    spotify_display_name: str
