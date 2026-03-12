import streamlit as st
st.set_page_config(page_title="Movie Recommendation System", layout="wide")
import os
from login import login_signup_screen


# Check login
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login_signup_screen()
    st.stop()

# === Sidebar ===
st.sidebar.title("📽 MENU")
st.sidebar.success(f"👤 Logged in as: {st.session_state['username']}")


if st.sidebar.button("🚪 Logout"):
    st.session_state["logged_in"] = False
    st.retrun()





st.sidebar.title("CONTENTS")


import os

# Function to open a new Streamlit page
def open_page(file_name):
    os.system(f"streamlit run {file_name}")

# Sidebar buttons to open specific pages
if st.sidebar.button("🎬 stream movie"):
    open_page("page.py")  # Opens purchase.py

if st.sidebar.button("🎞 Bollywood Movies"):
    open_page("bollywood.py")  # Opens bollywood.py

if st.sidebar.button("🎥 Hollywood Movies"):
    open_page("hollywood.py")  # Opens hollywood.pystreamlit rub



if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = None
if "selected_movie_id" not in st.session_state:
    st.session_state.selected_movie_id = None
if "movie_options" not in st.session_state:
    st.session_state.movie_options = []


# Function to get movie options (ID + Year)
def get_movie_options(movie_name):
    url = f"https://api.themoviedb.org/3/search/movie?api_key=93a7261b8594ec9d691f6bd21a977afc&query={movie_name}"
    response = requests.get(url).json()
    results = response.get("results", [])

    options = [(f"{movie['title']} ({movie.get('release_date', 'N/A')[:4]})", movie["id"]) for movie in results if
               "id" in movie]
    return options


def get_movie_trailer(movie_id):
    """
    Fetches the YouTube trailer link for a movie.
    """
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key=93a7261b8594ec9d691f6bd21a977afc"
    response = requests.get(url).json()

    for video in response.get("results", []):
        if video["type"] == "Trailer" and video["site"] == "YouTube":
            return f"https://www.youtube.com/watch?v={video['key']}"

    return None  # If no trailer is found


# Function to fetch movie details (Poster, Overview, IMDb Rating)
def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=93a7261b8594ec9d691f6bd21a977afc"
    response = requests.get(url).json()

    poster_path = response.get("poster_path", "")
    overview = response.get("overview", "No overview available.")
    imdb_rating = response.get("vote_average", "N/A")

    poster_url = f"http://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else "https://via.placeholder.com/500x750?text=No+Poster"

    return poster_url, overview, imdb_rating

import requests

def fetch_cast(movie_id):
    """
    Fetches the cast details (actors and their images) from TMDb.
    """
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=93a7261b8594ec9d691f6bd21a977afc"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        cast_names = []
        cast_images = []

        for actor in data.get("cast", [])[:5]:  # Fetch top 5 actors
            name = actor.get("name", "Unknown Actor")
            profile_path = actor.get("profile_path")

            if profile_path:
                full_profile_url = f"http://image.tmdb.org/t/p/w185/{profile_path}"
            else:
                full_profile_url = "https://via.placeholder.com/150x225?text=No+Image"  # Fallback image

            cast_names.append(name)``
            cast_images.append(full_profile_url)

        return cast_names, cast_images
    except requests.exceptions.RequestException as e:
        print(f"Error fetching cast details: {e}")
        return [], []


def fetch_actor_details(actor_name):
    """
    Fetch actor details using TMDb search and person endpoints.
    """
    search_url = f"https://api.themoviedb.org/3/search/person?api_key=93a7261b8594ec9d691f6bd21a977afc&query={actor_name}"
    search_response = requests.get(search_url).json()

    if search_response["results"]:
        person_id = search_response["results"][0]["id"]
        detail_url = f"https://api.themoviedb.org/3/person/{person_id}?api_key=93a7261b8594ec9d691f6bd21a977afc"
        detail_response = requests.get(detail_url).json()

        bio = detail_response.get("biography", "No biography available.")
        birthday = detail_response.get("birthday", "N/A")
        place = detail_response.get("place_of_birth", "N/A")

        return f"**Born:** {birthday}\n\n**Place:** {place}\n\n**Bio:** {bio[:400]}..."  # Limit bio length
    return "No details found."

# Function to fetch recommended movies
def fetch_recommendations(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key=93a7261b8594ec9d691f6bd21a977afc"
    response = requests.get(url).json()

    recommended_movies = []
    recommended_movies_posters = []

    for movie in response.get("results", [])[:5]:
        title = movie.get("title", "Unknown Title")
        poster_path = movie.get("poster_path", "")

        if poster_path:
            poster_url = f"http://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            poster_url = "https://via.placeholder.com/500x750?text=No+Poster"

        recommended_movies.append(title)
        recommended_movies_posters.append(poster_url)

    return recommended_movies, recommended_movies_posters


import streamlit as st

# Assuming you have the get_movie_options and fetch_movie_details functions already defined

import streamlit as st

# Movie search and API fetch
movie_name = st.text_input("Enter Movie Name")  # Allow user to enter the movie name

# Handle the search
if st.button("Search"):
    if movie_name.strip():  # Ensure that the movie name is not just empty spaces
        movie_options = get_movie_options(movie_name)
        st.session_state.movie_options = movie_options  # Store options in session
        st.session_state.selected_movie_id = None  # Reset selected movie ID
        st.session_state.selected_movie = None  # Reset selected movie name
        st.rerun()  # Refresh the page after search to show dropdown with options

# Show the movie options in the dropdown if available
if "movie_options" in st.session_state and st.session_state.movie_options:
    movie_selection = st.selectbox(
        "Select the correct movie:",
        st.session_state.movie_options,
        format_func=lambda x: x[0],  # Display movie title and year (or any format you prefer)
        key="movie_selection_box"
    )

    if movie_selection:
        st.session_state.selected_movie = movie_selection[0]  # Store name (Title + Year)
        st.session_state.selected_movie_id = movie_selection[1]  # Store correct ID
        st.session_state.movie_options = []  # Clear movie options after selection
        st.rerun()  # Refresh the page to load the movie details

# Check if a movie has been selected
if "selected_movie" in st.session_state and st.session_state.selected_movie and "selected_movie_id" in st.session_state and st.session_state.selected_movie_id:
    # Fetch movie details after selecting the movie
    searched_movie_poster, searched_movie_overview, imdb_rating = fetch_movie_details(st.session_state.selected_movie_id)
    recommended_movies, recommended_movies_posters = fetch_recommendations(st.session_state.selected_movie_id)
    trailer_url = get_movie_trailer(st.session_state.selected_movie_id)
    cast_names, cast_images = fetch_cast(st.session_state.selected_movie_id)  # Fetch cast details

    # Store them in session state
    st.session_state.recommended_movies = recommended_movies
    st.session_state.recommended_movies_posters = recommended_movies_posters
    st.session_state.trailer_url = trailer_url
    st.session_state.cast_names = cast_names
    st.session_state.cast_images = cast_images

    # Display the selected movie details
    st.image(searched_movie_poster, caption=st.session_state.selected_movie, width=250)
    st.write(f"**IMDb Rating:** {imdb_rating} ⭐")
    st.write(f"**Overview:** {searched_movie_overview}")

    if trailer_url:
        st.write("### 🎬 Watch Trailer:")
        st.video(trailer_url)

    # Display cast and recommendations

    # --- CAST Section ---
    st.markdown(
        """
        <style>
        .recommended-title {
            font-size: 28px;
            font-weight: bold;
            color: gold;
            text-align: center;
            text-shadow: 2px 2px 10px rgba(255, 215, 0, 0.8);
            padding-bottom: 5px;
            border-bottom: 2px solid gold;
            margin-bottom: 20px;
        }
        </style>
        <p class="recommended-title">CAST</p>
        """,
        unsafe_allow_html=True
    )

    if "cast_names" in st.session_state and st.session_state.cast_names:
        cast_cols = st.columns(len(st.session_state.cast_names))

        for idx, (name, image) in enumerate(zip(st.session_state.cast_names, st.session_state.cast_images)):
            with cast_cols[idx]:
                st.image(image, caption=name, width=100)

                with st.expander(f" {name}"):
                    actor_info = fetch_actor_details(name)
                    st.markdown(f"### {name}")
                    st.image(image, width=150)
                    st.markdown(actor_info)

    # --- RECOMMENDED MOVIES Section ---
    st.markdown(
        """
        <style>
        .recommended-title {
            font-size: 28px;
            font-weight: bold;
            color: gold;
            text-align: center;
            text-shadow: 2px 2px 10px rgba(255, 215, 0, 0.8);
            padding-bottom: 5px;
            border-bottom: 2px solid gold;
            margin-bottom: 20px;
        }
        </style>
        <p class="recommended-title">RECOMMENDED MOVIES</p>
        """,
        unsafe_allow_html=True
    )

    if "recommended_movies" in st.session_state and st.session_state.recommended_movies:
        num_cols = 5
        cols = st.columns(num_cols)

        for idx, (movie_title, movie_poster) in enumerate(
                zip(st.session_state.recommended_movies, st.session_state.recommended_movies_posters)):
            with cols[idx % num_cols]:
                st.image(movie_poster, caption=movie_title, width=150)
                if st.button(f" {movie_title}", key=f"rec_{idx}"):
                    # Set the selected movie again when a recommended movie is clicked
                    st.session_state.selected_movie = movie_title
                    st.session_state.selected_movie_id = get_movie_options(movie_title)[0][1]
                    st.rerun()  # Rerun to refresh movie details
