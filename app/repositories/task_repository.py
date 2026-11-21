from sqlalchemy.orm import Session

from app.models.task import Task


class TaskRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Task).all()

    def get_by_id(self, task_id: int):
        return self.db.query(Task).filter(Task.id == task_id).first()

    def create(self, title: str) -> Task:
        task = Task(title=title, completed=False)

        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)

        return task

    def update(self, task: Task, data: dict) -> Task:
        for key, value in data.items():
            setattr(task, key, value)

        self.db.commit()
        self.db.refresh(task)

        return task

    def delete(self, task: Task) -> None:
        self.db.delete(task)
        self.db.commit()