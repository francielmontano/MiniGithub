from datetime import datetime, timezone
from sqlalchemy import DateTime, String, Text, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database.base import Base

class Repository(Base):
    __tablename__ = "repository"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    is_private: Mapped[bool] = mapped_column(
        Boolean,
        default = False
    )

    owner_id = Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )


    __table_args__ = (
        UniqueConstraint("owner_id", "name", name="uq_owner_repo_name"),
    )