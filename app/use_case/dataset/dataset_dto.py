from app.use_case.base_dto import BaseDto
from app.use_case.base_schema import CamelBaseModel


class DatasetDto(BaseDto, CamelBaseModel):
    file_name: str
    created_at: str
    updated_at: str
