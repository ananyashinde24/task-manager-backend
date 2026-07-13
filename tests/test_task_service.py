import pytest
from unittest.mock import AsyncMock

from services.task_service import TaskService
from models.Task import Task



@pytest.fixture
def repository():
    return AsyncMock()


@pytest.fixture
def service(repository):
    return TaskService(repository)



@pytest.mark.asyncio
async def test_create_task_success(service, repository):

    task = Task(
        title="Learn FastAPI",
        description="Service Layer",
        status="Pending",
    )

    repository.create_task.return_value = task

    result = await service.create_task(task)

    assert result.title == "Learn FastAPI"
    assert result.description == "Service Layer"
    assert result.status == "Pending"

    repository.create_task.assert_awaited_once_with(task)


@pytest.mark.asyncio
async def test_create_task_repository_exception(service, repository):

    task = Task(
        title="FastAPI",
        description="Testing",
        status="Pending",
    )

    repository.create_task.side_effect = Exception("Database Error")

    with pytest.raises(Exception, match="Database Error"):
        await service.create_task(task)

    repository.create_task.assert_awaited_once_with(task)



@pytest.mark.asyncio
async def test_get_all_tasks_empty(service, repository):

    repository.get_all_tasks.return_value = []

    tasks = await service.get_all_tasks()

    assert tasks == []

    repository.get_all_tasks.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_all_tasks_multiple(service, repository):

    repository.get_all_tasks.return_value = [
        Task(
            task_id=1,
            title="Task One",
            description="Description One",
            status="Pending",
        ),
        Task(
            task_id=2,
            title="Task Two",
            description="Description Two",
            status="Completed",
        ),
    ]

    tasks = await service.get_all_tasks()

    assert len(tasks) == 2
    assert tasks[0].title == "Task One"
    assert tasks[1].title == "Task Two"

    repository.get_all_tasks.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_all_tasks_repository_exception(service, repository):

    repository.get_all_tasks.side_effect = ConnectionError("Database Down")

    with pytest.raises(ConnectionError, match="Database Down"):
        await service.get_all_tasks()

    repository.get_all_tasks.assert_awaited_once()


# =====================================================
# GET TASK BY ID
# =====================================================

@pytest.mark.asyncio
async def test_get_task_by_id_success(service, repository):

    repository.get_task_by_id.return_value = Task(
        task_id=1,
        title="Learn Testing",
        description="Pytest",
        status="Pending",
    )

    task = await service.get_task_by_id(1)

    assert task.task_id == 1
    assert task.title == "Learn Testing"
    assert task.description == "Pytest"

    repository.get_task_by_id.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_get_task_by_id_not_found(service, repository):

    repository.get_task_by_id.return_value = None

    task = await service.get_task_by_id(100)

    assert task is None

    repository.get_task_by_id.assert_awaited_once_with(100)


# =====================================================
# UPDATE TASK
# =====================================================

@pytest.mark.asyncio
async def test_update_task_success(service, repository):

    updates = {
        "title": "Updated Title",
        "status": "Completed",
    }

    repository.update_task.return_value = Task(
        task_id=1,
        title="Updated Title",
        description="Old Description",
        status="Completed",
    )

    task = await service.update_task(1, updates)

    assert task.title == "Updated Title"
    assert task.status == "Completed"

    repository.update_task.assert_awaited_once_with(
        1,
        updates,
    )


@pytest.mark.asyncio
async def test_update_task_not_found(service, repository):

    updates = {
        "title": "Updated"
    }

    repository.update_task.return_value = None

    result = await service.update_task(100, updates)

    assert result is None

    repository.update_task.assert_awaited_once_with(
        100,
        updates,
    )


@pytest.mark.asyncio
async def test_update_task_repository_exception(service, repository):

    updates = {
        "title": "Updated"
    }

    repository.update_task.side_effect = Exception("Update Failed")

    with pytest.raises(Exception, match="Update Failed"):
        await service.update_task(1, updates)

    repository.update_task.assert_awaited_once()


# =====================================================
# DELETE TASK
# =====================================================

@pytest.mark.asyncio
async def test_delete_task_success(service, repository):

    repository.delete_task_by_id.return_value = True

    result = await service.delete_task_by_id(1)

    assert result is True

    repository.delete_task_by_id.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_delete_task_not_found(service, repository):

    repository.delete_task_by_id.return_value = None

    result = await service.delete_task_by_id(100)

    assert result is None

    repository.delete_task_by_id.assert_awaited_once_with(100)


@pytest.mark.asyncio
async def test_delete_task_repository_exception(service, repository):

    repository.delete_task_by_id.side_effect = Exception("Delete Failed")

    with pytest.raises(Exception, match="Delete Failed"):
        await service.delete_task_by_id(1)

    repository.delete_task_by_id.assert_awaited_once_with(1)


# =====================================================
# DELETE ALL TASKS
# =====================================================

@pytest.mark.asyncio
async def test_delete_all_tasks_success(service, repository):

    repository.delete_all_tasks.return_value = True

    result = await service.delete_all_tasks()

    assert result is True

    repository.delete_all_tasks.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_all_tasks_repository_exception(service, repository):

    repository.delete_all_tasks.side_effect = Exception("Database Error")

    with pytest.raises(Exception, match="Database Error"):
        await service.delete_all_tasks()

    repository.delete_all_tasks.assert_awaited_once()