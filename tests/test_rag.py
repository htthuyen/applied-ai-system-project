from unittest.mock import MagicMock, patch

from src.embedder import build_song_collection, song_to_text
from src.rag import explain_with_claude, parse_query_with_claude, retrieve_candidates


def make_sample_songs():
    return [
        {
            "id": 1,
            "title": "Sunrise City",
            "artist": "Neon Echo",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.82,
            "tempo_bpm": 118.0,
            "valence": 0.84,
            "danceability": 0.79,
            "acousticness": 0.18,
        },
        {
            "id": 2,
            "title": "Midnight Coding",
            "artist": "LoRoom",
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.42,
            "tempo_bpm": 78.0,
            "valence": 0.56,
            "danceability": 0.62,
            "acousticness": 0.71,
        },
        {
            "id": 3,
            "title": "Storm Runner",
            "artist": "Voltline",
            "genre": "rock",
            "mood": "intense",
            "energy": 0.91,
            "tempo_bpm": 152.0,
            "valence": 0.48,
            "danceability": 0.66,
            "acousticness": 0.10,
        },
    ]


# --- embedder tests ---

def test_song_to_text_contains_key_fields():
    song = make_sample_songs()[0]
    text = song_to_text(song)
    assert "Sunrise City" in text
    assert "pop" in text
    assert "happy" in text
    assert "0.82" in text


def test_build_collection_has_correct_count():
    songs = make_sample_songs()
    collection = build_song_collection(songs, collection_name="test_songs")
    assert collection.count() == len(songs)


def test_retrieve_candidates_returns_k():
    songs = make_sample_songs()
    collection = build_song_collection(songs, collection_name="test_retrieve")
    results = retrieve_candidates("chill lofi for studying", collection, k=2)
    assert len(results) == 2
    assert all("title" in s and "genre" in s for s in results)


def test_retrieve_candidates_returns_dicts_with_required_fields():
    songs = make_sample_songs()
    collection = build_song_collection(songs, collection_name="test_fields")
    results = retrieve_candidates("upbeat pop", collection, k=1)
    song = results[0]
    for field in ["id", "title", "artist", "genre", "mood", "energy"]:
        assert field in song


# --- rag.py tests (Claude calls mocked) ---

def test_parse_query_returns_dict():
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text='{"genre_hint": "lofi", "mood_hint": "chill", "energy_hint": 0.3}')]

    with patch("src.rag._get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = parse_query_with_claude("something chill for studying")

    assert isinstance(result, dict)
    assert "genre_hint" in result
    assert "mood_hint" in result
    assert "energy_hint" in result


def test_parse_query_handles_bad_json():
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="not valid json")]

    with patch("src.rag._get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = parse_query_with_claude("anything")

    assert result == {"genre_hint": None, "mood_hint": None, "energy_hint": None}


def test_explain_returns_non_empty_string():
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="These songs match your vibe perfectly.")]

    with patch("src.rag._get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = explain_with_claude("chill beats", make_sample_songs()[:2])

    assert isinstance(result, str)
    assert result.strip() != ""
