import streamlit as st
import pickle
import gzip
import os
import requests
import gdown
import streamlit.components.v1 as components

# ==========================
# Google Drive file IDs
# ==========================
URL_SIMILARITY = "https://drive.google.com/uc?export=download&id=1NaMtpA10T260WwUFrcgwbgAzPUsF0YKx"  # similarity.pkl.gz
URL_MOVIES = "https://drive.google.com/uc?export=download&id=1tZ3q28hXsr0B-WuMyhQSR3v4AqtFzCgd"  # movies_list.pkl

# ==========================
# Download files if not exists
# ==========================
if not os.path.exists("similarity.pkl.gz"):
    gdown.download(URL_SIMILARITY, "similarity.pkl.gz", quiet=False)

if not os.path.exists("movies_list.pkl"):
    gdown.download(URL_MOVIES, "movies_list.pkl", quiet=False)

# ==========================
# Load pickle data
# ==========================
with gzip.open("similarity.pkl.gz", "rb") as f:
    similarity = pickle.load(f)

with open("movies_list.pkl", "rb") as f:
    movies = pickle.load(f)

movies_list = movies['title'].values

# ==========================
# TMDB Poster function
# ==========================
TMDB_API_KEY = "c7ec19ffdd3279641fb606d19ceb9bb1"

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    return None

# ==========================
# Streamlit UI
# ==========================
st.set_page_config(page_title="Hệ Thống Gợi Ý Phim", layout="wide")
st.header("Hệ Thống Gợi Ý Phim")

# Image carousel component (frontend/public)
imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")

# Example posters for carousel
example_movie_ids = [1632, 299536, 17455, 2830, 429422, 9722, 13972, 240, 155, 598, 914, 255709, 572154]
imageUrls = [fetch_poster(mid) for mid in example_movie_ids if fetch_poster(mid) is not None]

imageCarouselComponent(imageUrls=imageUrls, height=200)

# Movie selection box
selected_movie = st.selectbox("Chọn phim từ danh sách", movies_list)

# Recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    recommended_posters = []
    for i in distances[1:6]:  # top 5
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters

# Show recommendations
if st.button("Gợi Ý"):
    movie_names, movie_posters = recommend(selected_movie)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        col.text(movie_names[idx])
        if movie_posters[idx]:
            col.image(movie_posters[idx])
