from typing import Generic, Type, TypeVar

from model.base import BaseModel
from sqlalchemy.orm import Query, Session

T = TypeVar("T", bound=BaseModel)


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    def _query(self, session: Session, *_: ..., **kwargs: ...) -> Query[T]:
        filters = [getattr(self.model, k) == v for k, v in kwargs.items()]
        return session.query(self.model).filter(*filters)  # type: ignore

    def get(self, session: Session, *_: ..., **kwargs: ...) -> T | None:
        return self._query(session, **kwargs).one_or_none()  # type: ignore

    def get_many(self, session: Session, *_: ..., **kwargs: ...) -> list[T]:
        return self._query(session, **kwargs).all()  # type: ignore

    def create(self, session: Session, obj_in: ...) -> T:
        raise NotImplementedError
