from typing import List
from domain.entity.track import Track
import torch
import torch.nn.functional as F
import pickle
import pandas as pd
import numpy as np
import librosa
import re

def load_mel(path, sr=22050, n_mels=128, duration=30):
    y, sr = librosa.load(path, sr=sr, duration=duration)
    mel = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels)
    mel = librosa.power_to_db(mel)
    return mel

def fix_length(mel, target_len=1300):
    T = mel.shape[1]
    if T > target_len:
        return mel[:, :target_len]
    if T < target_len:
        pad = np.zeros((mel.shape[0], target_len - T), dtype=mel.dtype)
        return np.concatenate([mel, pad], axis=1)
    return mel

def recommend_similar(query_emb: torch.Tensor, track_embeddings: dict, exclude_ids=None):
    """Находим ближайший трек по косинусной схожести"""
    exclude_ids = exclude_ids or []
    best_id = None
    best_sim = -float('inf')
    for tid, emb in track_embeddings.items():
        if tid in exclude_ids:
            continue
        sim = F.cosine_similarity(query_emb, emb, dim=0).item()
        if sim > best_sim:
            best_sim = sim
            best_id = tid
    return best_id

def extract_track_id_from_filename(filename: str) -> int | None:
    """
    '000002.mp3' -> 2
    Returns None if filename doesn't match expected pattern.
    """
    MP3_PATTERN = re.compile(r"(\d+)\.mp3$", re.IGNORECASE)
    m = MP3_PATTERN.search(filename)
    if not m:
        return None
    return int(m.group(1)) 

class RecommendationModel:
    def __init__(self, model_path="recommender_model.pkl", embeddings_parquet="after_model_parquet.parquet"):
        with open(model_path, "rb") as f:
            self.model = pickle.load(f)
        self.model.eval()

        df = pd.read_parquet(embeddings_parquet)
        self.track_embeddings = {
            int(row.track_id): torch.tensor(row[2:], dtype=torch.float32)
            for row in df.itertuples()
        }

        audio_features = pd.read_parquet(audio_features.parquet)
        self.track_embeddings_features = {
            int(row.track_id): torch.tensor(row[2:], dtype=torch.float32)
            for row in audio_features.itertuples()
        }


        self.TARGET_LEN = 1300  

    def pick_next(self, likes: List[Track]) -> str:
        next_track_id = self.__predict(likes)
        return self.__build_path(next_track_id)

    def __predict(self, likes: List[Track]) -> int:
        """Используем трансформер для последовательности последних треков"""
        last_tracks = likes[-3:] 
        
        mel_seq = []
        meta_seq = []

        for track in last_tracks:
            track_id = extract_track_id_from_filename(track.id)
            mel = fix_length(load_mel(track.local_path), self.TARGET_LEN)
            mel_seq.append(mel)

            emb = self.track_embeddings_features[track_id] 
            meta_seq.append(emb)
            
        mel_tensor = torch.from_numpy(np.stack(mel_seq)).float().unsqueeze(1)  
        meta_tensor = torch.tensor(np.stack(meta_seq), dtype=torch.float32)     

        with torch.no_grad():
            pred_emb = self.model.forward(mel_tensor, meta_tensor)  
        pred_emb = pred_emb[-1] 
        pred_emb = pred_emb / (pred_emb.norm() + 1e-9)  

        exclude_ids = [extract_track_id_from_filename(track.id) for track in last_tracks]  
        next_track_id = recommend_similar(pred_emb, self.track_embeddings, exclude_ids)
        return next_track_id

    @staticmethod
    def __build_path(track_id: int) -> str:
        return f"/app/data/fma_small/{track_id:06d}/{track_id:06d}.mp3"
