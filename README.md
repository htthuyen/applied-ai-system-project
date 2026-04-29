# 🎵 VibeMatch — AI Music Recommender

> Describe your vibe in plain English. Get matched songs instantly.

---

## Original Project 

The original project was a **Music Recommender Simulation** built in Modules 3. It took a manually defined user profile — genre, mood, and energy level — and scored every song in a 20-song CSV catalog using a weighted formula: genre match (50%), mood match (30%), and energy proximity (20%). The system returned a ranked top-5 list with explanations for why each song scored the way it did. It worked well as a learning exercise but required users to know exactly what genre and mood they wanted, and it could only match exactly — "indie pop" got zero credit for a "pop" song.

---

## What VibeMatch Does

VibeMatch extends that original system with a **RAG (Retrieval-Augmented Generation)** pipeline powered by ChromaDB. Instead of filling out a form, users type a natural language description like *"something chill for late night studying"* and the system:

1. Embeds the entire song catalog into a vector store (ChromaDB)
2. Retrieves the most semantically similar songs using embedding search
3. Returns the top 5 matches ranked by semantic similarity

A **Classic mode** preserves the original dropdown-based interface for users who prefer manual control.

- A walk-through video:
<div>
    <a href="https://www.loom.com/share/85c292371346432aaf66ec58e30fd2b8">
    </a>
    <a href="https://www.loom.com/share/85c292371346432aaf66ec58e30fd2b8">
      <img style="max-width:300px;" src="https://cdn.loom.com/sessions/thumbnails/85c292371346432aaf66ec58e30fd2b8-6ab8711b50f37d67-full-play.gif#t=0.1">
    </a>
  </div>



---

## Architecture Overview

```
songs.csv ──► Embedder ──► ChromaDB (vector index, built once)

User query
  └──► ChromaDB semantic search ──► top-5 songs ──► User
```

![alt text](image.png)

| Component | File | Role |
|---|---|---|
| `song_to_text()` | `src/embedder.py` | Converts song metadata into embeddable text |
| `build_song_collection()` | `src/embedder.py` | Builds ChromaDB vector index from the catalog |
| `retrieve_candidates()` | `src/rag.py` | Runs semantic vector search, returns top-k songs |
| `score_song()` | `src/recommender.py` | Weighted re-ranking: genre 50% · mood 30% · energy 20% |
| `app.py` | root | Streamlit UI with RAG tab and Classic tab |


---

## Setup Instructions

### 1. Clone and create a virtual environment

```bash
git clone <your-repo-url>
cd applied-ai-system-project

python -m venv .venv
source .venv/bin/activate        # Mac / Linux
.venv\Scripts\activate           # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> The first run downloads the `all-MiniLM-L6-v2` embedding model (~80 MB) used by ChromaDB. This happens automatically and only once.

### 3. Run the Streamlit app

```bash
streamlit run app.py
```

Opens at **http://localhost:8501** automatically. No API key required.

### 4. Or use the command line

```bash
# Classic mode
python -m src.main

# RAG mode
python -m src.main --rag
```

### 5. Run tests

```bash
pytest
```

---

## Sample Interactions

### Example 1 — Late night study session (RAG mode)

**Input:**
```
something chill for late night studying
```

**Top results:**
```
#1  Library Rain · Paper Lanterns     lofi · chill · Energy 35%
#2  Midnight Coding · LoRoom          lofi · chill · Energy 42%
#3  Focus Flow · LoRoom               lofi · focused · Energy 40%
#4  Spacewalk Thoughts · Orbit Bloom  ambient · chill · Energy 28%
#5  Ocean Lanterns · Maris & Co.      folk · peaceful · Energy 33%
```

---

### Example 2 — Pre-workout energy (RAG mode)

**Input:**
```
upbeat and intense, I'm about to work out
```

**Top results:**
```
#1  Neon Drop · Kai Kinetic         edm · euphoric · Energy 95%
#2  Gym Hero · Max Pulse            pop · intense · Energy 93%
#3  Storm Runner · Voltline         rock · intense · Energy 91%
#4  Shadow Cathedral · Iron Hallow  metal · ominous · Energy 97%
#5  Midnight Salsa · Luna Brava     latin · playful · Energy 83%
```

---

### Example 3 — Classic mode

**Input:** Genre: `pop` · Mood: `happy` · Energy: `0.80`

**Top results:**
```
#1  Sunrise City · Neon Echo        Score: 1.16   pop · happy · Energy 82%
#2  Gym Hero · Max Pulse            Score: 1.04   pop · intense · Energy 93%
#3  Rooftop Lights · Indigo Parade  Score: 0.71   indie pop · happy · Energy 76%
#4  Midnight Salsa · Luna Brava     Score: 0.56   latin · playful · Energy 83%
#5  Neon Drop · Kai Kinetic         Score: 0.46   edm · euphoric · Energy 95%
```

---

## Design Decisions

### Why RAG instead of a pure keyword search?

Keyword search requires exact matches — "lofi" won't find a song tagged "ambient" even if the vibe is identical. RAG uses semantic embeddings so a query like *"something for the library at midnight"* finds songs that feel similar in meaning, not just in label.

### Why keep the original `score_song()` in Classic mode?

The weighted formula (genre 50%, mood 30%, energy 20%) was tuned and produces explainable, predictable results. Classic mode keeps that logic intact so users who know exactly what they want get consistent, transparent scoring.

### Why `all-MiniLM-L6-v2`?

It's a small (~80 MB), fast, local embedding model with strong semantic performance on short text. It runs entirely on your machine — no API key, no internet call after the initial download.

### Why ChromaDB in-memory instead of a persistent store?

The catalog has only 20 songs. There's no need for persistence between restarts — the index rebuilds in under a second. Using an in-memory client keeps setup to a single `pip install chromadb` with no external database server.

### Trade-offs

| Decision | Benefit | Cost |
|---|---|---|
| RAG over keyword search | Understands natural language | Requires embedding on startup |
| Local embeddings only | No API key, works offline | No LLM explanation of results |
| score_song in Classic mode | Consistent, explainable | Binary genre matching limits results |
| In-memory ChromaDB | Zero setup | Index lost on restart (fine for 20 songs) |

---

## Testing Summary

The project has **9 automated tests** across two files.

```
tests/test_recommender.py   2 tests   OOP Recommender class
tests/test_rag.py           7 tests   embedder + RAG pipeline
```

**What the tests cover:**

| Test | What it checks |
|---|---|
| `test_recommend_returns_songs_sorted_by_score` | Top result is the best genre + mood match |
| `test_explain_recommendation_returns_non_empty_string` | Explanation is a non-empty string |
| `test_song_to_text_contains_key_fields` | Text representation includes genre, mood, energy |
| `test_build_collection_has_correct_count` | ChromaDB stores all songs |
| `test_retrieve_candidates_returns_k` | Vector search returns exactly k results |
| `test_retrieve_candidates_returns_dicts_with_required_fields` | Each result has all expected keys |
| `test_parse_query_returns_dict` | Query parsing returns a valid dict |
| `test_parse_query_handles_bad_json` | Gracefully handles malformed responses |
| `test_explain_returns_non_empty_string` | Explanation returns a non-empty string |

---

## Reflection

Building VibeMatch taught me two things I didn't fully appreciate before.

**First, the gap between "structured data" and "human intent" is real and large.** The original system worked fine when users knew exactly what they wanted and could express it as `genre=lofi, mood=chill, energy=0.3`. But that's not how people think about music. They think in context: *"something for the library at midnight"* or *"I need to run faster."* Semantic embeddings bridge that gap — not by replacing the scoring logic, but by finding songs whose descriptions feel similar to the query.

**Second, you don't always need an LLM.** Early versions of this project used Claude to parse queries and explain results. But the core value — matching a vibe to a song — comes entirely from the embeddings. Removing the LLM layer made the system simpler, faster, free to run, and easier to test, with no meaningful loss in recommendation quality.

---

## Project Structure

```
applied-ai-system-project/
├── app.py                  # Streamlit UI (RAG tab + Classic tab)
├── data/
│   └── songs.csv           # 20-song catalog
├── src/
│   ├── embedder.py         # song_to_text, build_song_collection
│   ├── rag.py              # retrieve_candidates
│   ├── recommender.py      # Song, UserProfile, Recommender, score_song, recommend_songs
│   └── main.py             # CLI runner (--rag flag)
├── tests/
│   ├── test_recommender.py
│   └── test_rag.py
├── system_diagram.md       # Mermaid architecture diagram
├── model_card.md           # Original model card
└── requirements.txt
```
