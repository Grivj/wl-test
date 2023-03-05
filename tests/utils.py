from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app.model.base import BaseModel


def get_test_db() -> scoped_session:
    engine = create_engine("sqlite:///:memory:")
    session = sessionmaker(bind=engine)
    scoped = scoped_session(session)
    BaseModel.metadata.create_all(engine)  # type: ignore
    return scoped
