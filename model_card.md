# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

> Song 1.0

---

## 2. Intended Use

> This model suggests up to 5 songs from a 20-song catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

> The model scores each song by comparing it against the user's preferences across three features. Genre and mood are matched exactly — a match scores full points, a mismatch scores zero. Energy is scored by proximity: the closer the song's energy is to the user's target, the higher the score. Each feature is multiplied by a weight (genre: 0.50, mood: 0.30, energy: 0.20) and summed into a final score. Songs are then ranked from highest to lowest, and the top results are returned.

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

Building this system made it clear how much the design of a scoring rule shapes what users see. Choosing to weight genre at 0.50 × 2.0 meant that genre became the single most important factor — a decision that seemed reasonable but could easily be unfair to users whose taste cuts across genres. Human judgment matters not just in writing the algorithm, but in questioning the assumptions behind each weight. A model can only reflect the priorities its designer built into it, which is why transparency and the ability to explain every score are so important.
