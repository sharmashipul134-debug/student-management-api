import os
import tempfile
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import app as app_module


@pytest.fixture()
def client(monkeypatch):
    db_fd, db_path = tempfile.mkstemp()
    os.close(db_fd)
    monkeypatch.setattr(app_module, "DATABASE", db_path)
    monkeypatch.setattr(app_module, "API_KEY", "test-secret")
    app_module.app.config.update(TESTING=True)
    with app_module.app.test_client() as client:
        yield client
    os.unlink(db_path)


def headers():
    return {"X-API-Key": "test-secret"}


def test_home_and_health(client):
    assert client.get("/").status_code == 200
    assert client.get("/health").json["status"] == "ok"


def test_authentication_required(client):
    assert client.get("/students").status_code == 401


def test_crud_flow(client):
    response = client.post("/students", headers=headers(), json={
        "name": "Asha", "course": "BTech CSE", "email": "asha@example.com"
    })
    assert response.status_code == 201
    student_id = response.json["id"]

    assert client.get("/students", headers=headers()).status_code == 200
    assert client.get(f"/students/{student_id}", headers=headers()).json["name"] == "Asha"

    response = client.patch(f"/students/{student_id}", headers=headers(), json={"course": "BTech IT"})
    assert response.status_code == 200
    assert response.json["course"] == "BTech IT"

    assert client.delete(f"/students/{student_id}", headers=headers()).status_code == 200
    assert client.get(f"/students/{student_id}", headers=headers()).status_code == 404


def test_validation_and_duplicate_email(client):
    payload = {"name": "Asha", "course": "CSE", "email": "asha@example.com"}
    assert client.post("/students", headers=headers(), json={"name": "Asha"}).status_code == 400
    assert client.post("/students", headers=headers(), json=payload).status_code == 201
    assert client.post("/students", headers=headers(), json=payload).status_code == 409
