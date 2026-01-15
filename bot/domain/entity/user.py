from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum


@dataclass
class User:
    telegram_id: int
    id: Optional[int] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    favorite_music_genre: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)


class InteractionAction(str, Enum):
    skip = "skip"
    like = "like"
    dislike = "dislike"
