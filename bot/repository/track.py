from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from domain.entity.track import Track
from repository._orm import TrackORM


class TrackRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

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