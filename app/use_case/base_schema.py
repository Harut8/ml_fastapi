from enum import IntEnum

from pydantic import BaseModel, GetJsonSchemaHandler
from pydantic.alias_generators import to_camel
from pydantic_core import CoreSchema


class CamelBaseModel(BaseModel):
    class Config:
        alias_generator = to_camel


class BaseEnum(IntEnum):
    @classmethod
    def to_label_value(cls):
        return [
            {"label": cls.from_enum_mapping(_model.name), "value": _model.value} for _model in cls
        ]

    @property
    def str_value(self):
        return str(self._value_)

    @classmethod
    def from_enum_mapping(cls, _key):
        return cls._mapping[_key]

    @classmethod
    def __get_pydantic_json_schema__(cls, schema: CoreSchema, handler: GetJsonSchemaHandler):
        json_schema = handler(schema)
        json_schema = handler.resolve_ref_schema(json_schema)
        json_schema.update(
            {
                "enum": [x.value for x in cls],
                "type": "integer",
            }
        )
        return json_schema


def add_mapping_to_enum(_mapping: dict):
    def _wrapper(_enum):
        def __wrapper():
            _enum._mapping = _mapping
            return _enum

        return __wrapper()

    return _wrapper
