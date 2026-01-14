from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import (
    BigInteger,
    DateTime,
    Enum as SAEnum,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    Index,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from core.database import Base



class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)

    gender: Mapped[str] = mapped_column(String(1 << 4 - 1), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)

    favorite_music_genre: Mapped[str] = mapped_column(String(1 << 6 - 1), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    # relations
    interactions: Mapped[list["Interaction"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    feature_weights: Mapped[list["UserFeatureWeight"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class TrackORM(Base):
    __tablename__ = "tracks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(1 << 8 - 1), nullable=False)
    artist: Mapped[str] = mapped_column(String(1 << 8 - 1), nullable=False)
    album: Mapped[str | None] = mapped_column(String(1 << 8 - 1), nullable=True)

    duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)

    local_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    telegram_file_id: Mapped[str | None] = mapped_column(String(1 << 8 - 1), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    # relations
    interactions: Mapped[list["Interaction"]] = relationship(
        back_populates="track",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class InteractionORM(Base):
    __tablename__ = "interactions"
    __table_args__ = (
        Index("ix_interactions_user_created_at", "user_id", "created_at"),
        # Index("ix_interactions_user_track_action", "user_id", "track_id", "action"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    track_id: Mapped[int] = mapped_column(
        ForeignKey("tracks.id", ondelete="CASCADE"),
        nullable=False,
    )

    action: Mapped[InteractionAction] = mapped_column(
        SAEnum(InteractionAction, name="interaction_action"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    # relations
    user: Mapped["User"] = relationship(back_populates="interactions")
    track: Mapped["Track"] = relationship(back_populates="interactions")


class UserFeatureWeightORM(Base):
    __tablename__ = "user_feature_weights"
    __table_args__ = (
        UniqueConstraint("user_id", "feature_key", name="uq_user_feature_key"),
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,  # composite PK is fine here (also enforces uniqueness)
    )
    feature_key: Mapped[str] = mapped_column(
        String(1 << 8 - 1),
        primary_key=True,
        nullable=False,
    )

    weight: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # relations
    user: Mapped["User"] = relationship(back_populates="feature_weights")