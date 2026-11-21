from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.task import (
    TaskSchema,
    TaskCreateSchema,
    TaskUpdateSchema,
)
from app.services.task_service import TaskService, TaskNotFoundError


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    return TaskService(db)


@router.get("/", response_model=list[TaskSchema])
def get_tasks(
    service: TaskService = Depends(get_task_service),
):
    return service.get_all()


@router.get("/{task_id}", response_model=TaskSchema)
def get_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
):
    try:
        return service.get_by_id(task_id)
    except TaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )


@router.post(
    "/",
    response_model=TaskSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    payload: TaskCreateSchema,
    service: TaskService = Depends(get_task_service),
):
    return service.create(payload.title)


@router.patch("/{task_id}", response_model=TaskSchema)
def update_task(
    task_id: int,
    payload: TaskUpdateSchema,
    service: TaskService = Depends(get_task_service),
):
    try:
        data = payload.model_dump(exclude_unset=True)
        return service.update(task_id, data)
    except TaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
):
    try:
        service.delete(task_id)
    except TaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
