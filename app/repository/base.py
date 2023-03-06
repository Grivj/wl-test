import uuid as uid
from typing import Generic, Type, TypeVar

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Query, Session

from app.model.base import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    def _query(self, session: Session, *args: ..., **kwargs: ...) -> "Query[T]":
        filters = [getattr(self.model, k) == v for k, v in kwargs.items()]
        filters.extend(iter(args))
        return session.query(self.model).filter(*filters)  # type: ignore

    def get(self, session: Session, *args: ..., **kwargs: ...) -> T | None:
        return self._query(session, *args, **kwargs).one_or_none()  # type: ignore

    def get_many(self, session: Session, *args: ..., **kwargs: ...) -> list[T]:
        return self._query(session, *args, **kwargs).all()

    def create(self, session: Session, model: T) -> T:
        try:
            session.add(model)  # type: ignore
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise e
        return model

    def get_by_id(self, session: Session, id: uid.UUID) -> T | None:
        return self.get(session, id=id)

    def update(self, session: Session, model: T) -> T:
        session.commit()
        return model

    def delete(self, session: Session, model: T) -> None:
        session.delete(model)  # type: ignore
        session.commit()

    def delete_many(self, session: Session, models: list[T]) -> None:
        for model in models:
            session.delete(model)  # type: ignore
        session.commit()
