from sqlalchemy.orm import Session

from app.models.task import Task
from app.repositories.task_repository import TaskRepository


class TaskNotFoundError(Exception):
    pass


class TaskService:

    def __init__(self, db: Session):
        self.repository = TaskRepository(db)

    def get_all(self) -> list[Task]:
        return self.repository.get_all()

    def get_by_id(self, task_id: int) -> Task:
        task = self.repository.get_by_id(task_id)

        if task is None:
            raise TaskNotFoundError("Task not found")

        return task

    def create(self, title: str) -> Task:
        return self.repository.create(title)

    def update(self, task_id: int, data: dict) -> Task:
        task = self.get_by_id(task_id)

        return self.repository.update(task, data)

    def delete(self, task_id: int) -> None:
        task = self.get_by_id(task_id)

        self.repository.delete(task)
