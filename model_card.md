# 🎧 Model Card - VibeMatch

## 1. Model Name

> VibeMatch 2.0

---

## 2. Intended Use

> This model suggests up to 5 songs from a 20-song catalog based on a natural language description of what the user wants to hear. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

> The system has two modes. In **RAG mode**, each song in the catalog is converted into a text description and embedded into a local vector store (ChromaDB) using the `all-MiniLM-L6-v2` model. When a user types a natural language query, ChromaDB finds the 5 songs whose embeddings are closest to the query embedding and returns them. No API key or internet connection is required after the model downloads once. In **Classic mode**, the user selects genre, mood, and energy manually. The system scores each song using a weighted formula (genre: 0.50, mood: 0.30, energy: 0.20) and returns the top 5.

---

## 4. Data

The catalog contains 20 songs stored in `data/songs.csv`. Each song has 10 attributes: id, title, artist, genre, mood, energy, tempo, valence, danceability, and acousticness. The original starter dataset had 10 songs; 10 more were added to increase genre diversity, covering pop, lofi, rock, jazz, ambient, synthwave, indie pop, classical, hip hop, country, r&b, edm, metal, folk, latin, blues, and reggae.

---

## 5. Strengths

- Simple and transparent — every score can be traced back to exactly which features matched and by how much
- Easy to adjust — changing a weight or user profile immediately changes the output in an understandable way
- Good for learning — the system makes the logic of a recommender visible, which is useful for understanding how real systems work at a conceptual level

---

## 6. Limitations and Bias

- **Genre dominance** — with a raw score of 2.0 and a weight of 0.50, a genre match contributes 1.0 to the score. Songs without a genre match are capped at 0.50 regardless of how well they fit on mood and energy.
- **Binary genre matching** — genres are matched exactly, so "indie pop" and "pop" are treated as completely different even though they are closely related.
- **Small catalog** — 20 songs is too small to serve diverse users. Some genres and moods appear only once, limiting what the system can recommend.
- **No personalization over time** — the system has no memory. It cannot learn from what a user plays, skips, or replays.

---

## 7. Evaluation

The system was evaluated by running it with a pop/happy/high-energy user profile and checking whether the output matched expectations. "Sunrise City" (pop, happy, energy 0.82) ranked first with a score of 0.98, which felt correct. "Gym Hero" ranked second despite a mood mismatch, because it matched genre and had strong energy and valence scores. This confirmed that genre dominates when it matches, and continuous features act as tiebreakers.

---

## 8. Future Work

- Add support for multiple users and "group vibe" recommendations
- Balance diversity so the system does not always return the closest match — sometimes variety matters
- Use more features such as tempo, valence, and danceability to reduce genre dominance
- Introduce partial genre matching (e.g., "indie pop" partially matches "pop")

---

## 9. Personal Reflection

### Limitations and Biases

The system has several meaningful limitations. The catalog is only 20 songs — far too small to serve diverse users, and some genres appear only once, which means certain queries will return mediocre matches simply because nothing better exists. In RAG mode, the embedding model (`all-MiniLM-L6-v2`) was trained on general English text, not music descriptions, so it may treat words like "chill" and "peaceful" as more different than a music listener would. In Classic mode, genre matching is binary — "indie pop" and "pop" score zero overlap — which penalizes closely related genres unfairly. Neither mode learns from user feedback, so the system cannot improve over time or adapt to individual taste.

### Potential Misuse and Prevention

A music recommender at this scale has limited misuse potential, but two cases are worth noting. First, if the catalog were editable, a bad actor could tag songs with misleading metadata to manipulate what surfaces for a given query. Preventing this requires validating and locking the catalog to trusted sources. Second, the embedding model could reflect cultural biases in what it considers "similar" — for example, associating certain vibes with certain demographics in ways the system designer didn't intend. Auditing retrieval results across diverse queries before deployment would help surface these patterns.

### What Surprised Me During Testing

The biggest surprise was how sensitive ChromaDB was to collection naming. During testing, reusing the same collection name across test functions caused state to bleed between tests — a test that should have stored 5 songs was seeing results from a previous test's 20-song collection. The fix was simple (pass a unique `collection_name` per test) but the failure was silent — no error, just wrong counts. This taught me that in-memory stores are not as stateless as they feel when test isolation is not enforced explicitly. I also did not expect the embedding model to handle vague queries as well as it did — *"something for a rainy afternoon"* returned folk and acoustic songs without any explicit genre or mood label pointing there.

### Collaboration with AI

I used Claude as a coding assistant throughout this project. One instance where it was genuinely helpful was when I asked how to structure the RAG pipeline — it suggested separating the embedding logic (`embedder.py`) from the retrieval and generation logic (`rag.py`) rather than putting everything in one file. That separation made it much easier to test each part independently and mock only what needed mocking.

One instance where its suggestion was flawed was early on, when it suggested keeping Claude in the pipeline to re-rank the retrieved songs by parsing the query into structured genre and mood hints. In practice this added complexity without meaningfully improving results — the embedding search already captured the right vibe, and re-ranking with binary genre matching actually hurt results for queries that crossed genre boundaries. Removing Claude from the pipeline entirely produced cleaner, simpler code and results that were just as good.
