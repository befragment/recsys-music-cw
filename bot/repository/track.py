from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession


class TrackRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


