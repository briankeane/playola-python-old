from pydantic import BaseModel


class ClientPayloadSchema(BaseModel):
    url: str
