import uuid as uid

from sqlalchemy import Column
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import as_declarative  # type: ignore[import]


class CustomUUID(postgresql.UUID):
    python_type = uid.UUID  # type: ignore[assignment]


@as_declarative()  # type: ignore[call-arg]
class BaseModel:
    id = Column(
        CustomUUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uid.uuid4,
    )
