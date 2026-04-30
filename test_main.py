from fastapi.testclient import TestClient
import pytest
from main import app, tasks_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def limpar_banco():
    """Limpa o banco de dados antes de cada teste."""
    tasks_db.clear()
    import main

    main.task_counter = 1
    yield
    tasks_db.clear()


# Teste 1 — Rota raiz retorna status ok
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "message" in data


# Teste 2 — Health check retorna healthy
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


# Teste 3 — Criar uma tarefa com sucesso
def test_criar_tarefa():
    payload = {
        "id": 1,
        "title": "Tarefa de teste",
        "description": "Descrição da tarefa",
        "completed": False,
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Tarefa de teste"
    assert data["completed"] == False


# Teste 4 — Listar tarefas retorna lista vazia inicialmente
def test_listar_tarefas_vazio():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


# Teste 5 — Listar tarefas após criação
def test_listar_tarefas_com_dados():
    client.post("/tasks", json={"id": 1, "title": "Tarefa 1", "completed": False})
    client.post("/tasks", json={"id": 2, "title": "Tarefa 2", "completed": False})
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 2


# Teste 6 — Atualizar status de uma tarefa
def test_atualizar_tarefa():
    client.post("/tasks", json={"id": 1, "title": "Tarefa", "completed": False})
    response = client.put("/tasks/1?completed=true")
    assert response.status_code == 200
    assert response.json()["completed"] == True


# Teste 7 — Atualizar tarefa inexistente retorna 404
def test_atualizar_tarefa_inexistente():
    response = client.put("/tasks/999?completed=true")
    assert response.status_code == 404
    assert response.json()["detail"] == "Tarefa não encontrada"


# Teste 8 — Deletar uma tarefa com sucesso
def test_deletar_tarefa():
    client.post("/tasks", json={"id": 1, "title": "Tarefa", "completed": False})
    response = client.delete("/tasks/1")
    assert response.status_code == 204


# Teste 9 — Deletar tarefa inexistente retorna 404
def test_deletar_tarefa_inexistente():
    response = client.delete("/tasks/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Tarefa não encontrada"


# Teste 10 — Criar tarefa com ID automático (id=0)
def test_criar_tarefa_id_automatico():
    payload = {"id": 0, "title": "Tarefa automática", "completed": False}
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    assert response.json()["id"] != 0
