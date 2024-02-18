from typing import Optional

from pydantic import BaseModel, ConfigDict

class Track(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  id: int
  spotify_id: str
  title: str
  album: str
  duration_ms: int
  isrc: Optional[str]
  popularity: Optional[int]
  spotify_image_link: Optional[str]


class CuratorTrackWithTrack(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  id: int
  curator_id: int
  track: Track
  approved: bool
  
