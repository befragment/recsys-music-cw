from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entity.user import User
from domain.entity.song import Track
from domain.entity.interaction import InteractionType
from repository._orm import UserORM, TrackORM, InteractionORM


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User):
        """Создать пользователя"""
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        result = await self.session.execute(
            select(UserORM)
            .where(UserORM.telegram_id == telegram_id)
        )
        user_orm = result.scalar_one_or_none()
        if user_orm is None:
            return None
        return User(telegram_id=user_orm.telegram_id)

    async def get_user_id_by_telegram_id(self, telegram_id: int) -> int:
        """Получить ID пользователя по Telegram ID"""
        result = await self.session.execute(
            select(UserORM.id)
            .where(UserORM.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()

    async def get_telegram_id_by_user_id(self, user_id: int) -> int:
        """Получить Telegram ID пользователя по ID"""
        result = await self.session.execute(
            select(UserORM.id)
            .where(UserORM.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()

    async def get_user_tracks(self, user_id: int) -> List[Track]:
        """Получить все треки, с которыми взаимодействовал пользователь"""
        result = await self.session.execute(
            select(TrackORM)
            .join(InteractionORM, InteractionORM.track_id == TrackORM.id)
            .where(InteractionORM.user_id == user_id)
            .distinct()
        )
        track_orms = result.scalars().all()
        return [
            Track(
                id=track.id,
                title=track.title,
                artist=track.artist,
                duration=track.duration_ms or 0,
                album=track.album or ""
            )
            for track in track_orms
        ]

    async def get_liked_tracks(self, user_id: int) -> List[Track]:
        """Получить все треки, которые пользователь лайкнул"""
        result = await self.session.execute(
            select(TrackORM)
            .join(InteractionORM, InteractionORM.track_id == TrackORM.id)
            .where(InteractionORM.user_id == user_id, 
                   InteractionORM.interaction == InteractionType.LIKE))

        track_orms = result.scalars().all()
        return [
            Track(
                id=track.id,
                title=track.title,
                artist=track.artist,
                duration=track.duration_ms or 0,
                album=track.album or ""
            )
            for track in track_orms
        ]

    async def get_disliked_tracks(self, user_id: int) -> List[Track]:
        """Получить все треки, которые пользователь дизлайкнул"""
        result = await self.session.execute(
            select(TrackORM)
            .join(InteractionORM, InteractionORM.track_id == TrackORM.id)
            .where(InteractionORM.user_id == user_id, 
                   InteractionORM.interaction == InteractionType.DISLIKE))

        track_orms = result.scalars().all()
        return [
            Track(
                id=track.id,
                title=track.title,
                artist=track.artist,
                duration=track.duration_ms or 0,
                album=track.album or ""
            )
            for track in track_orms
        ]
