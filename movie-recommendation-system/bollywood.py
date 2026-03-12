import streamlit as st
import requests

st.set_page_config(layout="wide")

API_KEY = "93a7261b8594ec9d691f6bd21a977afc"
BASE_URL = "https://api.themoviedb.org/3"
POSTER_PATH = "https://image.tmdb.org/t/p/w200"

# Function to fetch popular Indian (Bollywood) movies
def fetch_bollywood_movies(pages=5):
    movies = []
    for page in range(1, pages + 1):
        url = f"{BASE_URL}/discover/movie?api_key=93a7261b8594ec9d691f6bd21a977afc&language=en-IN&region=IN&sort_by=popularity.desc&page={page}&with_original_language=hi"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            movies.extend(data["results"])
    return movies

# Scrollable view
st.markdown("<h2>Bollywood Movie Gallery</h2>", unsafe_allow_html=True)
movies = fetch_bollywood_movies(50)  # ~1000 movies

# Display posters with buttons
with st.container():
    for i in range(0, len(movies), 5):
        cols = st.columns(5)
        for j, col in enumerate(cols):
            if i + j < len(movies):
                movie = movies[i + j]
                with col:
                    st.image(f"{POSTER_PATH}{movie['poster_path']}", use_container_width=True)
                    if st.button(movie['title'], key=movie['id']):
                        movie_id = movie['id']
                        details = requests.get(
                            f"{BASE_URL}/movie/{movie_id}?api_key=93a7261b8594ec9d691f6bd21a977afc&language=en-US").json()

                        trailer_res = requests.get(
                            f"{BASE_URL}/movie/{movie_id}/videos?api_key=93a7261b8594ec9d691f6bd21a977afc&language=hi-en"
                        ).json()
                        trailer_key = ""
                        for vid in trailer_res["results"]:
                            if vid["type"] == "Trailer" and vid["site"] == "YouTube":
                                trailer_key = vid["key"]
                                break

                        st.markdown(f"### {movie['title']}")
                        st.markdown(f"**Overview**: {details.get('overview', 'No overview available.')}")
                        st.markdown(f"**IMDb Rating**: {details.get('vote_average', 'N/A')}")
                        if trailer_key:
                            st.video(f"https://www.youtube.com/watch?v={trailer_key}")
