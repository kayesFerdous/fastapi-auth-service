from fastapi.testclient import TestClient
import logging

logger = logging.getLogger(__name__)


def test_read_all_tasks(client: TestClient, test_user):
    token = test_user["token"]
    headers = {"Authorization": f"Bearer {token}"}

    client.post("/tasks/", json={"title": "Task 1", "description": "First"}, headers=headers)
    client.post("/tasks/", json={"title": "Task 2", "description": "Second"}, headers=headers)

    response  = client.get('/tasks/',headers=headers)
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2


def test_read_task_by_id(client: TestClient, test_user):
    token = test_user["token"]
    headers = {"Authorization": f"Bearer {token}"}

    client.post("/tasks/", json={"title": "Task 1", "description": "First"}, headers=headers)
    client.post("/tasks/", json={"title": "Task 2", "description": "Second"}, headers=headers)

    response  = client.get('/tasks/',headers=headers)
    assert response.status_code == 200
    data = response.json()

    response = client.get(f"/tasks/{data[0]['id']}", headers=headers)    
    logger.info(f"{response.json()}")
    assert response.json()['id'] == data[0]['id']
