import streamlit as st

st.set_page_config(page_title="VibeMatch", page_icon="🎵", layout="centered")


# ── Cached resources (run once) ──────────────────────────────────────────────

@st.cache_resource(show_spinner="Loading songs and building index...")
def load_and_index():
    from src.recommender import load_songs
    from src.embedder import build_song_collection
    songs = load_songs("data/songs.csv")
    collection = build_song_collection(songs)
    return songs, collection


# ── Shared UI helper ─────────────────────────────────────────────────────────

def show_song_card(rank: int, song: dict) -> None:
    st.markdown(f"**#{rank}  {song['title']}**  ·  *{song['artist']}*")
    st.caption(
        f"🎸 {song['genre'].title()}  ·  "
        f"😊 {song['mood'].title()}  ·  "
        f"⚡ Energy {song['energy']:.0%}"
    )
    st.divider()


# ── Page header ──────────────────────────────────────────────────────────────

st.title("🎵 VibeMatch")
st.caption("Describe your vibe — get AI-matched songs instantly.")
st.write("")

tab_rag, tab_classic = st.tabs(["🤖 RAG  ·  natural language", "⚙️ Classic  ·  manual filters"])


# ── TAB 1 — RAG mode ─────────────────────────────────────────────────────────

with tab_rag:
    st.write("")

    query = st.text_input(
        "What do you want to hear?",
        placeholder="e.g. chill lofi for late night studying",
    )

    if st.button("Find Songs", type="primary", use_container_width=True, key="rag_btn"):
        if not query.strip():
            st.warning("Please enter a description.")
        else:
            songs, collection = load_and_index()

            from src.rag import retrieve_candidates

            with st.spinner("Searching the catalog..."):
                top5 = retrieve_candidates(query, collection, k=5)

            st.subheader("Top Picks")
            for i, song in enumerate(top5, 1):
                show_song_card(i, song)


# ── TAB 2 — Classic mode ──────────────────────────────────────────────────────

with tab_classic:
    st.write("")

    songs, _ = load_and_index()

    genres = sorted(set(s["genre"] for s in songs))
    moods  = sorted(set(s["mood"]  for s in songs))

    col1, col2 = st.columns(2)
    with col1:
        genre = st.selectbox("Genre", genres)
        mood  = st.selectbox("Mood",  moods)
    with col2:
        energy = st.slider("Energy level", 0.0, 1.0, 0.7, 0.05)
        st.caption("0.0 = very calm  ·  1.0 = very intense")

    if st.button("Find Songs", type="primary", use_container_width=True, key="classic_btn"):
        from src.recommender import recommend_songs

        results = recommend_songs(
            {"genre": genre, "mood": mood, "energy": energy},
            songs,
            k=5,
        )

        st.subheader("Top Picks")
        for i, (song, sc, _) in enumerate(results, 1):
            col_info, col_score = st.columns([4, 1])
            with col_info:
                st.markdown(f"**#{i}  {song['title']}**  ·  *{song['artist']}*")
                st.caption(
                    f"🎸 {song['genre'].title()}  ·  "
                    f"😊 {song['mood'].title()}  ·  "
                    f"⚡ Energy {song['energy']:.0%}"
                )
            with col_score:
                st.metric("Score", f"{sc:.2f}")
            st.divider()
