from sqlalchemy.orm import Mapped

from app.entity.base import BaseModel


class DefaultDataset(BaseModel):
    file_name: Mapped[str]
