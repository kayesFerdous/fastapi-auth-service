from fastapi.testclient import TestClient
import logging


logger = logging.getLogger(__name__)


def get_token(client: TestClient, email: str):
    response = client.post(
        "/auth/login",
        data={"username": f"{email}", "password": "testpassword"},
    )
    token = response.json()["access_token"]
    return (token, response.status_code)



def test_read_all_users(client: TestClient, test_user):
    response = client.get("/users/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1


def test_update_existing_user(client: TestClient, test_user):
    response = client.put(
        f"/users/me",
        headers={"Authorization": f"Bearer {test_user['token']}"},
        json={"username": "test_updt"},
    )

    assert response.status_code == 200
    data = response.json()
    logger.info(f" data after updaing: ----------------------\n{data}")


def test_delete_existing_user(client: TestClient, test_user):
    response = client.delete(
        f"/users/me",
        headers={"Authorization": f"Bearer {test_user['token']}"},
    )

    assert response.status_code == 204

    

    

