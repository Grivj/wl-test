from typing import Generic, Type, TypeVar

from pydantic import BaseModel as PydanticBaseModel

from app.model.base import BaseModel

T = TypeVar("T", bound=BaseModel)
TSchema = TypeVar("TSchema", bound=PydanticBaseModel)


class Serializer(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    def serialize(self, model: T, schema: Type[TSchema]) -> TSchema:
        return schema.from_orm(model)

    def serialize_many(self, models: list[T], schema: Type[TSchema]) -> list[TSchema]:
        return [self.serialize(model, schema) for model in models]

    def deserialize(self, schema: PydanticBaseModel) -> T:
        return self.model(**schema.dict())

    def deserialize_many(self, schemas: list[TSchema]) -> list[T]:
        return [self.deserialize(schema) for schema in schemas]
