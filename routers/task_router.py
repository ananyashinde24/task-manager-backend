from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db

from models.Task import Task
from repository.task_repository import TaskRepository
from schemas.task_schema import TaskCreate, TaskUpdate
from services.task_service import TaskService

import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.post("/")
async def create_task(
    task: TaskCreate,
    db: AsyncSession = Depends(get_db),
):

    logger.info(
        "Received request to create task '%s'.",
        task.title,
    )

    repository = TaskRepository(db)
    service = TaskService(repository)

    task_model = Task(
        title=task.title,
        description=task.description,
    )

    response = await service.create_task(task_model)

    logger.info(
        "Task creation request completed."
    )

    return response


@router.get("/")
async def get_all_tasks(
    db: AsyncSession = Depends(get_db),
):

    logger.info(
        "Received request to fetch all tasks."
    )

    repository = TaskRepository(db)
    service = TaskService(repository)

    response = await service.get_all_tasks()

    logger.info(
        "Fetch all tasks request completed."
    )

    return response


@router.get("/{task_id}")
async def get_task_by_id(
    task_id: int,
    db: AsyncSession = Depends(get_db),
):

    logger.info(
        "Received request to fetch task with ID %d.",
        task_id,
    )

    repository = TaskRepository(db)
    service = TaskService(repository)

    response = await service.get_task_by_id(task_id)

    logger.info(
        "Fetch task request completed for task ID %d.",
        task_id,
    )

    return response


@router.patch("/{task_id}")
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: AsyncSession = Depends(get_db),
):

    logger.info(
        "Received request to update task with ID %d.",
        task_id,
    )

    repository = TaskRepository(db)
    service = TaskService(repository)

    updates = task_data.model_dump(exclude_unset=True)

    response = await service.update_task(
        task_id,
        updates,
    )

    logger.info(
        "Update task request completed for task ID %d.",
        task_id,
    )

    return response


@router.delete("/")
async def delete_all_tasks(
    db: AsyncSession = Depends(get_db),
):

    logger.warning(
        "Received request to delete all tasks."
    )

    repository = TaskRepository(db)
    service = TaskService(repository)

    response = await service.delete_all_tasks()

    logger.warning(
        "Delete all tasks request completed."
    )

    return response


@router.delete("/{task_id}")
async def delete_task_by_id(
    task_id: int,
    db: AsyncSession = Depends(get_db),
):

    logger.info(
        "Received request to delete task with ID %d.",
        task_id,
    )

    repository = TaskRepository(db)
    service = TaskService(repository)

    response = await service.delete_task_by_id(task_id)

    logger.info(
        "Delete task request completed for task ID %d.",
        task_id,
    )

    return response