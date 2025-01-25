from fastapi.testclient import TestClient
from ..main import app
from fastapi import status

tester_client = TestClient(app)


def test_return_health_check():
    response = tester_client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "Healthy"}
