from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_send_email():
    response = client.post("/email", json={"email": "test@example.com"})
    assert response.status_code == 200
    assert response.json() == {"message": "email has been sent"}
