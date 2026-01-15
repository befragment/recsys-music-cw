from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from domain.entity.track import Track
from repository._orm import TrackORM


class TrackRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_track_by_id(self, track_id: int) -> Track | None:
        try:
            result = await self.session.execute(select(TrackORM).where(TrackORM.id == track_id))
            track_orm = result.scalar_one_or_none()
            if track_orm is None:
                return None
            return Track(
                id=track_orm.id,
                title=track_orm.title,
                artist=track_orm.artist,
                duration=track_orm.duration_ms or 0,
                album=track_orm.album or "",
                local_path=track_orm.local_path,
            )
        finally:
            await self.session.close()

    async def get_all_tracks(self) -> List[Track]:
        try:
            result = await self.session.execute(select(TrackORM))
            return [
                Track(
                    id=track.id,
                    title=track.title,
                    artist=track.artist,
                    duration=track.duration_ms or 0,
                    album=track.album or "",
                    local_path=track.local_path,
                )
                for track in result.scalars().all()
            ]
        finally:
            await self.session.close()

    async def get_track_by_path(self, path: str) -> Track | None:
        try:
            result = await self.session.execute(select(TrackORM).where(TrackORM.local_path == path))
            track_orm = result.scalar_one_or_none()
            if track_orm is None:
                return None
            return Track(
                id=track_orm.id,
                title=track_orm.title,
                artist=track_orm.artist,
                duration=track_orm.duration_ms or 0,
                album=track_orm.album or "",
                local_path=track_orm.local_path,
            )
        finally:
            await self.session.close()