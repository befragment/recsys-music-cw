from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entity.user import User
from domain.entity.track import Track
from domain.entity.interaction import InteractionAction
from repository._orm import UserORM, TrackORM, InteractionORM


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User):
        """Создать пользователя"""
        try:
            user_orm = UserORM(
                telegram_id=user.telegram_id,
                gender=user.gender,
                age=user.age,
                favorite_music_genre=user.favorite_music_genre,
            )
            self.session.add(user_orm)
            await self.session.commit()
            await self.session.refresh(user_orm)
            return User(
                telegram_id=user_orm.telegram_id,
                gender=user_orm.gender,
                age=user_orm.age,
                favorite_music_genre=user_orm.favorite_music_genre,
            )
        finally:
            await self.session.close()

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        try:
            result = await self.session.execute(
                select(UserORM).where(UserORM.telegram_id == telegram_id)
            )
            user_orm = result.scalar_one_or_none()
            if user_orm is None:
                return None
            return User(telegram_id=user_orm.telegram_id)
        finally:
            await self.session.close()

    async def get_user_id_by_telegram_id(self, telegram_id: int) -> int | None:
        """Получить ID пользователя по Telegram ID"""
        try:
            result = await self.session.execute(
                select(UserORM.id).where(UserORM.telegram_id == telegram_id)
            )
            return result.scalar_one_or_none()
        finally:
            await self.session.close()

    async def get_telegram_id_by_user_id(self, user_id: int) -> int | None:
        """Получить Telegram ID пользователя по ID"""
        try:
            result = await self.session.execute(
                select(UserORM.telegram_id).where(UserORM.id == user_id)
            )
            return result.scalar_one_or_none()
        finally:
            await self.session.close()

    async def get_user_tracks(self, user_id: int) -> List[Track]:
        """Получить все треки, с которыми взаимодействовал пользователь"""
        try:
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
                    album=track.album or "",
                    local_path=track.local_path,
                )
                for track in track_orms
            ]
        finally:
            await self.session.close()

    async def get_liked_tracks(self, user_id: int) -> List[Track]:
        """Получить все треки, которые пользователь лайкнул"""
        try:
            result = await self.session.execute(
                select(TrackORM)
                .join(InteractionORM, InteractionORM.track_id == TrackORM.id)
                .where(
                    InteractionORM.user_id == user_id,
                    InteractionORM.action == InteractionAction.like,
                )
            )

            track_orms = result.scalars().all()
            return [
                Track(
                    id=track.id,
                    title=track.title,
                    artist=track.artist,
                    duration=track.duration_ms or 0,
                    album=track.album or "",
                    local_path=track.local_path,
                )
                for track in track_orms
            ]
        finally:
            await self.session.close()

    async def get_disliked_tracks(self, user_id: int) -> List[Track]:
        """Получить все треки, которые пользователь дизлайкнул"""
        try:
            result = await self.session.execute(
                select(TrackORM)
                .join(InteractionORM, InteractionORM.track_id == TrackORM.id)
                .where(
                    InteractionORM.user_id == user_id,
                    InteractionORM.action == InteractionAction.dislike,
                )
            )

            track_orms = result.scalars().all()
            return [
                Track(
                    id=track.id,
                    title=track.title,
                    artist=track.artist,
                    duration=track.duration_ms or 0,
                    album=track.album or "",
                    local_path=track.local_path,
                )
                for track in track_orms
            ]
        finally:
            await self.session.close()
