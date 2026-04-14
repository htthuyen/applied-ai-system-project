# 🎵 Music Recommender Simulation

## Project Summary

This project simulates a music recommender system. Given a user's preferences, the system scores every song in the catalog and returns a ranked list of the best matches. User preferences are defined by three features: genre, mood, and energy.

---

## How The System Works

Most successful music recommender systems are built by combining users' behavioral signals (likes, dislikes, skips, replays, etc.), item metadata, and context. They also apply collaborative filtering ("people like you liked this") and content-based filtering ("you liked X, here are items like X").

Based on the given dataset, this system uses **content-based filtering** with two rules:

- **Scoring rule** — `score_song(user_prefs, song)` computes how well a single song matches the user. It uses a weighted sum of three features:
  - Genre match (binary: 2.0 if match, 0.0 if not) × 0.50
  - Mood match (binary: 1.0 if match, 0.0 if not) × 0.30
  - Energy proximity (1 − |song energy − user energy|) × 0.20

- **Ranking rule** — `recommend_songs(user_prefs, songs, k)` calls `score_song` on every song, sorts all results by score in descending order, and returns the top `k` recommendations.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

- **Raised genre raw score from 1.0 to 2.0** — A genre match now contributes 1.0 to the final score (0.50 × 2.0) instead of 0.50. This widened the gap between genre-matching and non-matching songs, making genre the dominant factor in ranking. Songs without a genre match are capped at a score of 0.50 no matter how well they fit on mood and energy.

---

## Limitations and Risks

- **Genre bias** — genre carries the most weight (0.50 × 2.0 = 1.0), so the system strongly favors genre-matching songs. In real life, users may care more about energy or mood than genre, and this system would not serve them well.
- **Small catalog** — the dataset has only 20 songs. With so few options, the top results are constrained regardless of how well the scoring logic works.
- **No behavioral signals** — the system relies entirely on a manually defined user profile. It has no way to learn from what a user actually plays, skips, or replays.
- **Binary genre matching** — a user who likes "indie pop" gets zero genre credit for a "pop" song, even though the genres are closely related.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

I am amazed by how powerful data is. I have learned that the better data we have, the more robust recommender system become. Diversity in the dataset is especially important - without it, the system can only serve users whose preferences are already well represented, leaving others with poor recommendations.
