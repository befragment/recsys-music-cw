from pathlib import Path

from service._contract import TrackRepositoryProtocol


class TrackService:
    def __init__(self, track_repository: TrackRepositoryProtocol):
        self.track_repository = track_repository


def track_path_in_fs(
    root: str | Path | None = None, 
    track_id: int | None = None
) -> Path:
    root = Path(root)
    tid = f"{track_id:06d}"
    return root / tid[:3] / f"{tid}.mp3"


if __name__ == "__main__":
    print(track_path("data/fma_small", 148002))  # data/fma_small/148/148002.mp3