from pathlib import Path

from service._contract import TrackRepositoryProtocol


class TrackService:
    def __init__(self, track_repository: TrackRepositoryProtocol):
        self.track_repository = track_repository


def track_id_to_path(
    root: str | Path | None = "data/fma_small", 
    track_id: int | None = None
) -> Path:
    root = Path(root)
    tid = f"{track_id:06d}"
    return root / tid[:3] / f"{tid}.mp3"


if __name__ == "__main__":
    print(track_id_to_path(148002))  # data/fma_small/148/148002.mp3
    