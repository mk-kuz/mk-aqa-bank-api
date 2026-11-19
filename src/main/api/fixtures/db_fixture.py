from collections.abc import Generator

import pytest
from sqlalchemy.orm import Session

from src.main.api.db.engine import SessionLocal, engine


@pytest.fixture(scope='function')
def db_session() -> Generator[Session, None, None]:
    conn = engine.connect()
    transaction = conn.begin()
    session = SessionLocal(bind=conn)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        conn.close()
