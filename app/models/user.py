from datetime import datetime
from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from ..database.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(39),
        unique=True,
    )

    email: Mapped[str] = mapped_column(
        String(255), 
        unique=True, index=True
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
    )

    avatar_url: Mapped[str | None] = mapped_column(
        String(500), 
        nullable=True
    )

    bio: Mapped[str | None] = mapped_column(
        nullable=True
    )

    website_url: Mapped[str | None] = mapped_column(
        String(255), 
        nullable=True
    )

    create_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    update_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
