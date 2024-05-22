import enum
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, MappedAsDataclass


class TODOSTATUS(enum.Enum):
    todo = "todo"
    completed = "completed"


class Base(DeclarativeBase, MappedAsDataclass):
    pass


class TODO(Base):
    __tablename__ = "todos"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    todo: Mapped[str] = mapped_column(unique=True)
    status: Mapped[TODOSTATUS]
