import chromadb
from typing import List, Dict


def retrieve_candidates(
    query: str, collection: chromadb.Collection, k: int = 10
) -> List[Dict]:
    """Retrieves top-k semantically similar songs from ChromaDB."""
    results = collection.query(query_texts=[query], n_results=k)

    songs = []
    for meta in results["metadatas"][0]:
        songs.append(
            {
                "id": int(meta["id"]),
                "title": meta["title"],
                "artist": meta["artist"],
                "genre": meta["genre"],
                "mood": meta["mood"],
                "energy": float(meta["energy"]),
                "tempo_bpm": float(meta["tempo_bpm"]),
                "valence": float(meta["valence"]),
                "danceability": float(meta["danceability"]),
                "acousticness": float(meta["acousticness"]),
            }
        )
    return songs
