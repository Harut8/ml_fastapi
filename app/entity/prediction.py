from sqlalchemy.orm import Mapped

from app.entity.base import BaseModel


class Training(BaseModel):
    pipe_line_name: Mapped[str]
    is_running: Mapped[int]