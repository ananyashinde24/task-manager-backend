from repository.task_repository import TaskRepository
from models.Task import Task

import logging

logger = logging.getLogger(__name__)


class TaskService:

    def __init__(self, repository: TaskRepository):
        self.repository = repository

    async def create_task(
        self,
        task_model: Task,
    ):

        logger.info(
            "Creating task '%s'.",
            task_model.title,
        )

        task = await self.repository.create_task(task_model)

        logger.info(
            "Task '%s' created successfully.",
            task.title,
        )

        return task

    async def get_all_tasks(self):

        logger.info(
            "Fetching all tasks."
        )

        tasks = await self.repository.get_all_tasks()

        logger.info(
            "Retrieved %d task(s).",
            len(tasks),
        )

        return tasks

    async def get_task_by_id(
        self,
        task_id: int,
    ):

        logger.info(
            "Fetching task with ID %d.",
            task_id,
        )

        task = await self.repository.get_task_by_id(task_id)

        if task is None:

            logger.warning(
                "Task with ID %d not found.",
                task_id,
            )

            return None

        logger.info(
            "Task with ID %d retrieved successfully.",
            task_id,
        )

        return task

    async def update_task(
        self,
        task_id: int,
        updates: dict,
    ):

        logger.info(
            "Updating task with ID %d.",
            task_id,
        )

        task = await self.repository.update_task(
            task_id,
            updates,
        )

        if task is None:

            logger.warning(
                "Update failed. Task with ID %d not found.",
                task_id,
            )

            return None

        logger.info(
            "Task with ID %d updated successfully.",
            task_id,
        )

        return task

    async def delete_all_tasks(self):

        logger.warning(
            "Deleting all tasks."
        )

        result = await self.repository.delete_all_tasks()

        logger.warning(
            "All tasks deleted successfully."
        )

        return result

    async def delete_task_by_id(
        self,
        task_id: int,
    ):

        logger.info(
            "Deleting task with ID %d.",
            task_id,
        )

        task = await self.repository.delete_task_by_id(
            task_id,
        )

        if task is None:

            logger.warning(
                "Delete failed. Task with ID %d not found.",
                task_id,
            )

            return None

        logger.info(
            "Task with ID %d deleted successfully.",
            task_id,
        )

        return task