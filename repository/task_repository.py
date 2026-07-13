from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.Task import Task

import logging

logger = logging.getLogger(__name__)


class TaskRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_task(self, task: Task):

        logger.info(
            "Creating task '%s'.",
            task.title,
        )

        self.db.add(task)

        await self.db.commit()

        await self.db.refresh(task)

        logger.info(
            "Task created successfully with ID %s.",
            task.task_id,
        )

        return task

    async def get_all_tasks(self):

        logger.debug("Fetching all tasks from database.")

        result = await self.db.execute(
            select(Task)
        )

        tasks = result.scalars().all()

        logger.info(
            "Retrieved %d task(s) from database.",
            len(tasks),
        )

        return tasks

    async def get_task_by_id(
        self,
        task_id: int,
    ):

        logger.debug(
            "Fetching task with ID %d.",
            task_id,
        )

        result = await self.db.execute(
            select(Task).where(
                Task.task_id == task_id
            )
        )

        task = result.scalar_one_or_none()

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

        task = await self.get_task_by_id(task_id)

        if task is None:
            return None

        logger.debug(
            "Applying updates %s to task %d.",
            updates,
            task_id,
        )

        for key, value in updates.items():

            if hasattr(task, key):
                setattr(task, key, value)

        await self.db.commit()

        await self.db.refresh(task)

        logger.info(
            "Task with ID %d updated successfully.",
            task_id,
        )

        return task

    async def delete_task_by_id(
        self,
        task_id: int,
    ):

        logger.info(
            "Deleting task with ID %d.",
            task_id,
        )

        task = await self.get_task_by_id(task_id)

        if task is None:
            return None

        await self.db.delete(task)

        await self.db.commit()

        logger.info(
            "Task with ID %d deleted successfully.",
            task_id,
        )

        return task

    async def delete_all_tasks(self):

        logger.warning(
            "Deleting all tasks from database."
        )

        result = await self.db.execute(
            select(Task)
        )

        tasks = result.scalars().all()

        for task in tasks:
            await self.db.delete(task)

        await self.db.commit()

        logger.info(
            "Deleted %d task(s) successfully.",
            len(tasks),
        )

        return "All tasks deleted successfully."