from pathlib import Path

def track_id_to_path(track_id: int, root: str = "data/fma_small") -> Path:
    root = Path(root)
    tid = f"{track_id:06d}"
    return root / tid[:3] / f"{tid}.mp3"


if __name__ == "__main__":
    print(track_id_to_path(148002))  # data/fma_small/148/148002.mp3
