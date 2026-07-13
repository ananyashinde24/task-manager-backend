import pytest

from models.Task import Task


def test_create_task_object():

    task = Task(
        title="Learn FastAPI",
        description="Testing Models",
        status="Pending",
    )

    assert task.title == "Learn FastAPI"
    assert task.description == "Testing Models"
    assert task.status == "Pending"


def test_default_status():

    task = Task(
        title="Learn SQLAlchemy",
        description="Defaults",
    )

    # SQLAlchemy default is applied when inserting into DB,
    # so before insert it may be None.
    assert task.status is None or task.status == "Pending"


def test_update_task_fields():

    task = Task(
        title="Old",
        description="Old Description",
        status="Pending",
    )

    task.title = "New"
    task.description = "New Description"
    task.status = "Completed"

    assert task.title == "New"
    assert task.description == "New Description"
    assert task.status == "Completed"


def test_task_id_assignment():

    task = Task(
        task_id=10,
        title="Testing",
        description="Pytest",
        status="Pending",
    )

    assert task.task_id == 10


def test_multiple_task_objects():

    task1 = Task(
        task_id=1,
        title="Task 1",
        description="One",
        status="Pending",
    )

    task2 = Task(
        task_id=2,
        title="Task 2",
        description="Two",
        status="Completed",
    )

    assert task1.task_id != task2.task_id
    assert task1.title != task2.title