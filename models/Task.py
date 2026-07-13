
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base






class Task(Base):

    __tablename__ = "tasks"

    task_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    title: Mapped[str] = mapped_column(
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        default="Pending",
        nullable=False,
    )







