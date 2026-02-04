import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from main import app, database, models

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def client():
    models.Base.metadata.create_all(bind=engine)

    with TestingSession() as db:
        role_admin = models.Role(description="Admin")
        role_dev = models.Role(description="Dev")
        db.add(role_admin)
        db.add(role_dev)
        db.commit()

    def override_get_db():
        try:
            db = TestingSession()
            yield db
        finally:
            db.close()

    app.dependency_overrides[database.get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
    models.Base.metadata.drop_all(bind=engine)
