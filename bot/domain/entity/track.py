from dataclasses import dataclass


@dataclass(frozen=True)
class Track:
    id: int
    title: str
    artist: str
    duration: int  # ms
    album: str
    local_path: str
