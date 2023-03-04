from typing import Any, Generic, Type, TypeVar

from sqlalchemy.orm import Query, Session

from app.model.base import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    def _query(self, session: Session, *_: ..., **kwargs: ...) -> "Query[T]":
        filters = [getattr(self.model, k) == v for k, v in kwargs.items()]
        return session.query(self.model).filter(*filters)  # type: ignore

    def get(self, session: Session, *_: ..., **kwargs: ...) -> T | None:
        return self._query(session, **kwargs).one_or_none()  # type: ignore

    def get_many(self, session: Session, *_: ..., **kwargs: ...) -> list[T]:
        return self._query(session, **kwargs).all()  # type: ignore

    def create(self, session: Session, obj_in: dict[str, Any] | T) -> T:
        if isinstance(obj_in, dict):
            return self._create_from_dict(session, obj_in)
        if isinstance(obj_in, self.model):
            return self._create_from_model(session, obj_in)
        raise TypeError(
            f"obj_in must be of type {self.model} or dict, not {type(obj_in)}"
        )

    def _create_from_model(self, session: Session, obj_in: T) -> T:
        return add_and_commit(session, obj_in)

    def _create_from_dict(self, session: Session, obj_in: dict[str, Any]) -> T:
        return add_and_commit(session, self.model(**obj_in))


class RepositoryException(Exception):
    pass


def add_and_commit(session: Session, obj: T) -> T:
    try:
        session.add(obj)  # type: ignore
        session.commit()
    except Exception as e:
        session.rollback()
        raise RepositoryException(
            f"Error while adding {obj} to session: {str(e)}"
        ) from e
    finally:
        return obj
