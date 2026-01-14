from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class User:
    telegram_id: int
    gender: str
    age: int
    favorite_music_genre: str
    created_at: datetime