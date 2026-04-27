import streamlit as st
import pickle
import requests

st.set_page_config(page_title="Movie Recommendation System", page_icon="🎬", layout="wide")

# ------------ Load Data ---------
movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

movie_list = movies["title"].values


# ----------- Fetch Poster -----------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=89214b375dd9a15327af92e478c5bff3&language=en-US"
    response = requests.get(url)
    data = response.json()

    if "poster_path" in data and data["poster_path"]:
        return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"


# ---------- Recommend Function -----------
def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]

    movies_list = similarity[movie_index][:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters


# ---------- Background Orbs(Waves) Only ------------
st.markdown("""
<style>
/* Fixed background orbs — nothing else changed */
.orb-container {
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}

.orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.35;
    animation: float linear infinite;
}

.orb-1 {
    width: 500px; height: 500px;
    background: radial-gradient(circle, rgba(99,102,241,0.6), transparent 70%);
    top: -150px; left: -100px;
    animation-duration: 18s;
    animation-delay: 0s;
}

.orb-2 {
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(168,85,247,0.55), transparent 70%);
    top: 40%; right: -100px;
    animation-duration: 22s;
    animation-delay: -6s;
}

.orb-3 {
    width: 350px; height: 350px;
    background: radial-gradient(circle, rgba(236,72,153,0.45), transparent 70%);
    bottom: -80px; left: 30%;
    animation-duration: 25s;
    animation-delay: -12s;
}

.orb-4 {
    width: 280px; height: 280px;
    background: radial-gradient(circle, rgba(59,130,246,0.5), transparent 70%);
    top: 20%; left: 55%;
    animation-duration: 20s;
    animation-delay: -4s;
}

.orb-5 {
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(16,185,129,0.4), transparent 70%);
    bottom: 20%; right: 25%;
    animation-duration: 28s;
    animation-delay: -9s;
}

@keyframes float {
    0%   { transform: translateY(0px) scale(1); }
    33%  { transform: translateY(-30px) scale(1.05); }
    66%  { transform: translateY(20px) scale(0.97); }
    100% { transform: translateY(0px) scale(1); }
}
.stApp {
    background: #28282B;
}
.stImage img {
    max-width: 87% !important;
}

.stImage + div p {
    font-size: 18px !important;
    color: white !important;
    font-weight: 500 !important;
}
</style>

<div class="orb-container">
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>
    <div class="orb orb-4"></div>
    <div class="orb orb-5"></div>
</div>
""", unsafe_allow_html=True)


# -------- Streamlit UI ---------
st.title("🎬 Movie Recommendation System")

selected_movie_name = st.selectbox(
    "Which movie would you like to watch?",
    movie_list
)

if st.button("Recommend"):
   with st.spinner("🎬 Finding movies for you..."):
    movie_names, movie_posters = recommend(selected_movie_name)

    st.subheader("Recommended Movies")

    # Row 1
    col1, col2, col3 = st.columns(3)

    with col1:
        st.image(movie_posters[0])
        st.markdown(f"<p style='color:white; font-size:18px; font-weight:500;'>{movie_names[0]}</p>", unsafe_allow_html=True)

    with col2:
        st.image(movie_posters[1])
        st.markdown(f"<p style='color:white; font-size:18px; font-weight:500;'>{movie_names[1]}</p>", unsafe_allow_html=True)

    with col3:
        st.image(movie_posters[2])
        st.markdown(f"<p style='color:white; font-size:18px; font-weight:500;'>{movie_names[2]}</p>", unsafe_allow_html=True)

    # Row 2
    col4, col5, col6 = st.columns(3)

    with col4:
        st.image(movie_posters[3])
        st.markdown(f"<p style='color:white; font-size:18px; font-weight:500;'>{movie_names[3]}</p>", unsafe_allow_html=True)

    with col5:
        st.image(movie_posters[4])
        st.markdown(f"<p style='color:white; font-size:18px; font-weight:500;'>{movie_names[4]}</p>", unsafe_allow_html=True)

    with col6:
        st.image(movie_posters[5])
        st.markdown(f"<p style='color:white; font-size:18px; font-weight:500;'>{movie_names[5]}</p>", unsafe_allow_html=True)
