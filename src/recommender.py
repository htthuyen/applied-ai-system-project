from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
        }
        scored = []
        for song in self.songs:
            score, _ = score_song(
                user_prefs,
                {"genre": song.genre, "mood": song.mood, "energy": song.energy},
            )
            scored.append((score, song))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [song for _, song in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
        }
        score, reasons = score_song(
            user_prefs,
            {"genre": song.genre, "mood": song.mood, "energy": song.energy},
        )
        reason_text = ", ".join(reasons) if reasons else "energy proximity only"
        return f"Score {score:.2f}: {reason_text}"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv
    songs = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    reasons = []
    score = 0.0

    # --- Categorical features (binary match) ---
    genre_score = 2.0 if song["genre"] == user_prefs["genre"] else 0.0
    if genre_score:
        reasons.append(f"genre matches '{user_prefs['genre']}'")

    mood_score = 1.0 if song["mood"] == user_prefs["mood"] else 0.0
    if mood_score:
        reasons.append(f"mood matches '{user_prefs['mood']}'")

    # --- Continuous features (proximity on 0-1 scale) ---
    energy_score = 1 - abs(song["energy"] - user_prefs["energy"])
    reasons.append(f"energy fit: {energy_score:.2f}")

    # --- Weighted sum (weights sum to 1.0) ---
    score = (
        0.50 * genre_score +
        0.30 * mood_score +
        0.20 * energy_score
    )

    return (score, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons)
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
