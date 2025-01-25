from .utils import *
from ..routers.admin import get_db
from fastapi import status
from ..models import Todos

app.dependency_overrides[get_db] = override_get_db


def test_admin_read_all(test_todo):
    response = tester_client.get("/admin/todo")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "complete": False,
            "title": "Learn to code!",
            "description": "Need to learn everyday!",
            "id": 1,
            "priority": 5,
        }
    ]


def test_admin_delete_todo(test_todo):
    response = tester_client.delete("/admin/todo/1")
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_admin_delete_todo_not_found():
    response = tester_client.delete("/admin/todo/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found."}
