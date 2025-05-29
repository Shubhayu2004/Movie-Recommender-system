import pickle
import streamlit as st
import requests

# --- Custom CSS for background and cards ---
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #232526 0%, #414345 100%);
        color: #fff;
    }
    .stButton>button {
        background-color: #e50914;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5em 2em;
        margin-top: 1em;
    }
    .movie-card {
        background: #222;
        border-radius: 12px;
        padding: 1em;
        margin: 0.5em 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        text-align: center;
    }
    .movie-title {
        font-size: 1.1em;
        font-weight: bold;
        margin: 0.5em 0 0.2em 0;
        color: #e50914;
    }
    </style>
""", unsafe_allow_html=True)

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except Exception:
        return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie_names, recommended_movie_posters

st.markdown("<h1 style='text-align: center; color: #e50914;'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #fff;'>Find your next favorite movie! Select a movie you like and get recommendations instantly.</p>", unsafe_allow_html=True)

movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list,
    index=0,
    key="movie_select"
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    st.markdown("<h3 style='color:#fff;'>Recommended for you:</h3>", unsafe_allow_html=True)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.markdown(f"<div class='movie-card'><img src='{recommended_movie_posters[idx]}' width='150' style='border-radius:8px;'/><div class='movie-title'>{recommended_movie_names[idx]}</div></div>", unsafe_allow_html=True)