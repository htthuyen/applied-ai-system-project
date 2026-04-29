"""
Command line runner for the Music Recommender Simulation.

Run classic mode:   python -m src.main
Run RAG mode:       python -m src.main --rag
"""

import sys

from src.recommender import load_songs, recommend_songs, score_song


def classic_mode() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 50)
    print("  Top Recommendations (classic mode)")
    print("=" * 50)

    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{i}  {song['title']} by {song['artist']}")
        print(f"    Score : {score:.2f}")
        print(f"    Genre : {song['genre']}  |  Mood: {song['mood']}")
        print(f"    Why   :")
        for reason in explanation.split(", "):
            print(f"            - {reason}")

    print("\n" + "=" * 50)


def rag_mode() -> None:
    from src.embedder import build_song_collection
    from src.rag import retrieve_candidates

    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs. Building vector index (first run downloads embedding model)...")

    collection = build_song_collection(songs)
    print("Index ready.\n")

    query = input("Describe what you want to hear: ").strip()
    if not query:
        print("No query entered.")
        return

    print("\nSearching...")

    top5 = retrieve_candidates(query, collection, k=5)

    print("\n" + "=" * 50)
    print("  Top Recommendations (RAG mode)")
    print("=" * 50)

    for i, song in enumerate(top5, start=1):
        print(f"\n#{i}  {song['title']} by {song['artist']}")
        print(f"    Genre : {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']:.0%}")

    print("\n" + "=" * 50)


def main() -> None:
    if "--rag" in sys.argv:
        rag_mode()
    else:
        classic_mode()


if __name__ == "__main__":
    main()
