import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict


def song_to_text(song: Dict) -> str:
    """Converts a song dict to a descriptive text string for embedding."""
    energy_label = (
        "high energy" if song["energy"] > 0.7
        else ("medium energy" if song["energy"] > 0.4 else "low energy")
    )
    return (
        f"{song['title']} by {song['artist']}. "
        f"Genre: {song['genre']}. "
        f"Mood: {song['mood']}. "
        f"{energy_label} ({song['energy']:.2f}). "
        f"Tempo: {song['tempo_bpm']:.0f} BPM."
    )


def build_song_collection(
    songs: List[Dict], collection_name: str = "songs"
) -> chromadb.Collection:
    """Builds an in-memory ChromaDB collection of embedded songs."""
    client = chromadb.Client()

    try:
        client.delete_collection(collection_name)
    except Exception:
        pass

    collection = client.create_collection(
        name=collection_name,
        embedding_function=embedding_functions.DefaultEmbeddingFunction(),
    )

    collection.add(
        documents=[song_to_text(s) for s in songs],
        ids=[str(s["id"]) for s in songs],
        metadatas=[
            {
                "id": str(s["id"]),
                "title": s["title"],
                "artist": s["artist"],
                "genre": s["genre"],
                "mood": s["mood"],
                "energy": float(s["energy"]),
                "tempo_bpm": float(s["tempo_bpm"]),
                "valence": float(s["valence"]),
                "danceability": float(s["danceability"]),
                "acousticness": float(s["acousticness"]),
            }
            for s in songs
        ],
    )

    return collection
