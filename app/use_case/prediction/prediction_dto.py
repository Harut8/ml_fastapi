from app.use_case.base_dto import BaseDto
from app.use_case.base_schema import CamelBaseModel


class ActivePipelineDto(BaseDto, CamelBaseModel):
    active_count: int = 0