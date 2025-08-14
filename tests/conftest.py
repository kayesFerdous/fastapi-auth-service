import asyncio

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool


from database import Base, get_db
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def override_get_db():
    # db = None  # Initialize db to None
    # try:
    #     db = TestingSessionLocal()
    #     yield db
    # finally:
    #     if db:  # Only close if db was successfully assigned
    #         db.close()
    async with TestingSessionLocal() as db:
        yield db

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def client():
    import asyncio
    # Create tables before tests
    async def create_tables():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(create_tables())

    with TestClient(app) as c:
        yield c

    # Drop tables after tests
    async def drop_tables():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    asyncio.run(drop_tables())


@pytest.fixture(scope="module")
def test_user(client: TestClient):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
        "role": "admin"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201, response.text
    new_user = response.json()

    response = client.post(
        "/auth/login",
        data={"username": user_data["email"], "password": user_data["password"]},
    )
    assert response.status_code == 200, response.text
    token = response.json()["access_token"]

    yield {"user": new_user, "token": token}
