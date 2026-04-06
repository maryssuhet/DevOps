from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_task():
    response = client.post(
        "/tasks",
        json={
            "id": 0,
            "title": "Estudar CI/CD",
            "description": "Concluir o projeto prático",
        },
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Estudar CI/CD"
    assert response.json()["id"] == 1


def test_get_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_update_task():
    # Assume que a tarefa com ID 1 existe (criada no teste anterior ou aqui)
    response = client.put("/tasks/1?completed=true")
    assert response.status_code == 200
    assert response.json()["completed"] == True


def test_delete_task():
    response = client.delete("/tasks/1")
    assert response.status_code == 204

    # Verifica se foi deletada
    response = client.get("/tasks")
    tasks = response.json()
    assert all(task["id"] != 1 for task in tasks)
