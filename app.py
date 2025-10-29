import os
import requests
import pickle
import streamlit as st
import streamlit.components.v1 as components

# -----------------------------
# Google Drive direct download links
# -----------------------------
URL_MOVIES = "https://drive.google.com/uc?export=download&id=1tZ3q28hXsr0B-WuMyhQSR3v4AqtFzCgd"
URL_SIMILARITY = "https://drive.google.com/uc?export=download&id=1NaMtpA10T260WwUFrcgwbgAzPUsF0YKx"

# -----------------------------
# Tải file .pkl nếu chưa có
# -----------------------------
if not os.path.exists("movies_list.pkl"):
    r = requests.get(URL_MOVIES)
    with open("movies_list.pkl", "wb") as f:
        f.write(r.content)

if not os.path.exists("similarity.pkl"):
    r = requests.get(URL_SIMILARITY)
    with open("similarity.pkl", "wb") as f:
        f.write(r.content)

# -----------------------------
# Load dữ liệu
# -----------------------------
movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['title'].values

# -----------------------------
# Streamlit UI
# -----------------------------
st.header("Hệ Thống Gợi Ý Phim")

# Carousel component
imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return None

# Demo poster carousel
imageUrls = [
    fetch_poster(1632),
    fetch_poster(299536),
    fetch_poster(17455),
    fetch_poster(2830),
    fetch_poster(429422),
    fetch_poster(9722),
    fetch_poster(13972),
    fetch_poster(240),
    fetch_poster(155),
    fetch_poster(598),
    fetch_poster(914),
    fetch_poster(255709),
    fetch_poster(572154)
]
imageUrls = [url for url in imageUrls if url]  # loại bỏ None
imageCarouselComponent(imageUrls=imageUrls, height=200)

# Chọn phim
selectvalue = st.selectbox("Chọn phim từ danh sách", movies_list)

# Hàm gợi ý phim
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommend_movie = []
    recommend_poster = []
    for i in distance[1:6]:
        movies_id = movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movies_id))
    return recommend_movie, recommend_poster

# Nút gợi ý
if st.button("Gợi Ý"):
    movie_name, movie_poster = recommend(selectvalue)
    col1, col2, col3, col4, col5 = st.columns(5)
    for col, name, poster in zip([col1, col2, col3, col4, col5], movie_name, movie_poster):
        col.text(name)
        col.image(poster)
