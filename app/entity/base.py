import datetime
import re
import uuid
from typing import TypeVar

import sqlalchemy
from pydantic.alias_generators import to_camel
from sqlalchemy import UUID, DateTime, func
from sqlalchemy.dialects.postgresql import ENUM as DEFAULT_PG_ENUM
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

_FACTORY_CLS = TypeVar("_FACTORY_CLS", bound="BaseModel")


def to_snake_case(name):
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    name = re.sub("__([A-Z])", r"_\1", name)
    name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name)
    return name.lower()


# todo: change uuid to id?
class BaseModel(DeclarativeBase):
    __abstract__ = True
    uuid = sqlalchemy.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    @declared_attr.directive
    def __tablename__(cls):
        return to_snake_case(cls.__name__)

    @classmethod
    def factory(cls: _FACTORY_CLS, **kwargs) -> _FACTORY_CLS:
        return cls(**kwargs)

    def to_dict(self, camel_case: bool = False):
        if camel_case:
            return {to_camel(c.name): getattr(self, c.name) for c in self.__table__.columns}
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def merge_tables_output(self, output):
        for c in output.__table__.columns:
            setattr(self, c.name, getattr(output, c.name))
        return self

    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

        return self


class PG_ENUM(DEFAULT_PG_ENUM):
    def __init__(self, *args, **kwargs):
        kwargs["values_callable"] = lambda obj: [str(e.value) for e in obj]
        super().__init__(*args, **kwargs)
