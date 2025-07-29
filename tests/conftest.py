import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import api

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = None  # Initialize db to None
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        if db:  # Only close if db was successfully assigned
            db.close()

api.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def client():
    # Create tables before tests
    Base.metadata.create_all(bind=engine)
    with TestClient(api) as c:
        yield c
    # Drop tables after tests
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def test_user(client: TestClient):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
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


# @pytest.fixture(scope="module")
# def test_task(client: TestClient, test_user):
#     # user_data = {
#     #     "username": "testuser",
#     #     "email": "test@example.com",
#     #     "password": "testpassword",
#     # }
#     # response = client.post("/users/", json=user_data)
#     #
#     # response = client.post(
#     #     "/auth/login",
#     #     data={"username": user_data["email"], "password": user_data["password"]},
#     # )
#     # assert response.status_code == 200
#     token = test_user["access_token"]
#     headers = {"Authorization": f"Bearer {token}"}
#
#     client.post("/tasks/", json={"title": "Task 1", "description": "First"}, headers=headers)
#     client.post("/tasks/", json={"title": "Task 2", "description": "Second"}, headers=headers)
#
#     task_data = {
#         "title": "testtask",
#         "description": "test description",
#         "is_done": False,
#     }
#     response = client.post(
#         "/tasks/", json=task_data, 
#         headers={"Authorization": f"Bearer {token}"},
#     )
#     assert response.status_code == 201, response.text
#     new_task = response.json()
#
#     yield {"task": new_task, "token": token}
