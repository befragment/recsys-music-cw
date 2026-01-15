"""initial schema

Revision ID: 001
Revises:
Create Date: 2026-01-15 13:30:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("telegram_id", sa.BigInteger(), nullable=False),
        sa.Column("gender", sa.String(length=15), nullable=False),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.Column("favorite_music_genre", sa.String(length=63), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("telegram_id"),
    )

    # Create tracks table
    op.create_table(
        "tracks",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("artist", sa.String(length=255), nullable=False),
        sa.Column("album", sa.String(length=255), nullable=True),
        sa.Column("duration_ms", sa.Integer(), nullable=True),
        sa.Column("local_path", sa.String(length=1024), nullable=False),
        sa.Column("telegram_file_id", sa.String(length=255), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create interactions table
    op.create_table(
        "interactions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("track_id", sa.Integer(), nullable=False),
        sa.Column(
            "action",
            postgresql.ENUM(
                "like", "dislike", "skip", "listen", name="interaction_action"
            ),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["track_id"], ["tracks.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_interactions_user_created_at",
        "interactions",
        ["user_id", "created_at"],
        unique=False,
    )
    op.create_index(
        "ix_interactions_user_track_action",
        "interactions",
        ["user_id", "track_id", "action"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_interactions_user_track_action", table_name="interactions")
    op.drop_index("ix_interactions_user_created_at", table_name="interactions")
    op.drop_table("interactions")
    op.drop_table("tracks")
    op.drop_table("users")
