
from sqlalchemy.orm import Session
import json

from app.services.redis_service import RedisService
from app.models.task import Task
from app.repositories.task_repository import TaskRepository


class TaskNotFoundError(Exception):
    pass


class TaskService:

    def __init__(self, db: Session):
        self.repository = TaskRepository(db)
        self.cache = RedisService()

    def get_all(self) -> list[Task]:
        cache_key = "tasks:all"
        cached_tasks = self.cache.get(cache_key)

        if cached_tasks is not None:
            return [
                Task(**task)
                for task in json.loads(cached_tasks)
            ]

        tasks = self.repository.get_all()

        data = [
            {
                "id": task.id,
                "title": task.title,
                "completed": task.completed,
            }
            for task in tasks
        ]

        self.cache.set(cache_key, json.dumps(data), expire=300)

        return tasks

    def get_by_id(self, task_id: int) -> Task:
        tasks = self.get_all()

        for task in tasks:
            if task.id == task_id:
                return task

        raise TaskNotFoundError("Task not found")

    def create(self, title: str) -> Task:
        task = self.repository.create(title)

        cached_tasks = self.cache.get("tasks:all")

        if cached_tasks is not None:
            tasks = json.loads(cached_tasks)

            tasks.append({
                "id": task.id,
                "title": task.title,
                "completed": task.completed,
            })

            self.cache.set(
                "tasks:all",
                json.dumps(tasks),
                expire=300,
            )

        return task

    def update(self, task_id: int, data: dict) -> Task:
        self.get_by_id(task_id)

        # Получаем ORM-объект из БД, а не из Redis.
        task = self.repository.get_by_id(task_id)
        task = self.repository.update(task, data)

        cached_tasks = self.cache.get("tasks:all")

        if cached_tasks is not None:
            tasks = json.loads(cached_tasks)

            updated_task = {
                "id": task.id,
                "title": task.title,
                "completed": task.completed,
            }

            tasks = [
                updated_task if item["id"] == task_id else item
                for item in tasks
            ]

            self.cache.set(
                "tasks:all",
                json.dumps(tasks),
                expire=300,
            )

        return task

    def delete(self, task_id: int) -> None:
        self.get_by_id(task_id)

        self.repository.delete(task_id)

        cached_tasks = self.cache.get("tasks:all")

        if cached_tasks is not None:
            tasks = [
                item
                for item in json.loads(cached_tasks)
                if item["id"] != task_id
            ]

            self.cache.set(
                "tasks:all",
                json.dumps(tasks),
                expire=300,
            )
