from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Gerenciador de Tarefas DevOps")

# Modelo de dados
class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

# Banco de dados em memória para exemplo
tasks_db = []
task_counter = 1

@app.get("/")
async def root():
    return {"status": "ok", "message": "API de Tarefas funcionando!", "version": "1.1.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    return tasks_db

@app.post("/tasks", response_model=Task, status_code=201)
async def create_task(task: Task):
    global task_counter
    # Se o ID não for passado ou for 0, geramos um automático (simplificado)
    if task.id == 0:
        task.id = task_counter
    
    tasks_db.append(task)
    task_counter = max(task_counter, task.id) + 1
    return task

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task_status(task_id: int, completed: bool):
    for task in tasks_db:
        if task.id == task_id:
            task.completed = completed
            return task
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")

@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int):
    global tasks_db
    new_db = [task for task in tasks_db if task.id != task_id]
    if len(new_db) == len(tasks_db):
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    tasks_db = new_db
    return None