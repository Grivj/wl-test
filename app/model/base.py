import uuid as uid

from sqlalchemy import Column, types
from sqlalchemy.ext.declarative import as_declarative  # type: ignore[import]


class CustomUUID(types.TypeDecorator[uid.UUID]):
    impl = types.CHAR

    def process_bind_param(self, value: uid.UUID | None, _):  # type: ignore[override]
        return None if value is None else str(value)

    def process_result_value(self, value: str | None, _) -> uid.UUID | None:  # type: ignore[override]
        return None if value is None else uid.UUID(str(value))


@as_declarative()  # type: ignore[call-arg]
class BaseModel:
    id = Column(
        CustomUUID,
        primary_key=True,
        index=True,
        default=uid.uuid4,
    )
