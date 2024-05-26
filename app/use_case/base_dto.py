import uuid

from pydantic import BaseModel, Field


class BaseDto(BaseModel):
    class Config:
        from_attributes = True
        populate_by_name = True


class IdBaseDto(BaseDto):
    id: uuid.UUID = Field(validation_alias="uuid")
