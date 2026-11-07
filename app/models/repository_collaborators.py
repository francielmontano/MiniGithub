from datetime import datetime, timezone
from sqlalchemy import DateTime, String, Boolean, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from ..database.base import Base

class Repository_Collaborators(Base):
    __tablename__ = "repository_collaborators"

    repository_id: Mapped[int] = mapped_column(
        ForeignKey("repository.id", ondelete="CASCADE"),
        primary_key=True
    )
    
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete = "CASCADE"),
        primary_key=True
    )
    
    role: Mapped[str] = mapped_column(
        String(20),
        default= "write", #roles pensados write, read and admin
        nullable= False
    )
    