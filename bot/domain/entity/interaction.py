from typing import Literal, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

@dataclass
class Interaction:
    user_id: int
    track_id: int
    action: InteractionAction
    occurred_at: datetime
    weight: float = 1.0


class InteractionAction(str, Enum):
    skip = "skip"
    like = "like"
    dislike = "dislike"


action_weights = {
    InteractionAction.skip: -0.3,
    InteractionAction.like: 1.0,
    InteractionAction.dislike: 1.0
}

