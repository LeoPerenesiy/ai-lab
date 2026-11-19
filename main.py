from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from uuid import uuid4

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

tasks = []

class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool

class TaskCreateSchema(BaseModel):
    title: str

@app.get("/tasks")
def read_tasks() -> list[TaskSchema]:
    return tasks

@app.post("/tasks")
def create_task(payload: TaskCreateSchema) -> TaskSchema:
    task = TaskSchema(id=str(uuid4()), title=payload.title, completed=False)
    tasks.append(task)
    return task

@app.get("/health")
async def healthcheck():
    return {"PY": 'Alive!'}