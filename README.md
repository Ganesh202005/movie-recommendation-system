# 🎬 Movie Recommendation System

A web application built with **Streamlit** that recommends movies using **The Movie Database (TMDb) API**. Users can search for movies, view detailed information, explore cast members, and get personalized recommendations.

Built by a **BCA student from Mumbai** passionate about film production, screenwriting, and technology projects.

---

# 🚀 Features

- User authentication with **Login / Signup system**
- Search movies by name and view:
  - Poster
  - Overview
  - IMDb rating
  - Trailer
  - Cast details
- View **Top 5 cast members** with expandable actor biographies
- Get **movie recommendations** based on the selected movie
- Sidebar navigation for **Bollywood / Hollywood movie browsing**
- Responsive and interactive UI built with **Streamlit**

---

# 📂 File Structure

| File | Description |
|-----|-------------|
| `main.py` | Core application with login, search, recommendations, and TMDb API integration |
| `login.py` | Handles user authentication |
| `bollywood.py` | Displays Bollywood movie recommendations |

---

# 🛠 Tech Stack

**Frontend / Backend**
- Streamlit

**API**
- TMDb API (movie details, cast, trailers)

**Database**
- SQLite

**Libraries**
- requests
- streamlit
- pandas

---

# ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/movie-recommendation-system.git
cd movie-recommendation-system
```

### 2️⃣ Install Dependencies

```bash
pip install streamlit requests pandas
```

### 3️⃣ Get TMDb API Key

Create a free API key from:

https://www.themoviedb.org/

Replace the API key in `main.py`.

```python
TMDB_API_KEY = "your_api_key"
```

---

# ▶️ Run the Application

```bash
streamlit run main.py
```

Open in browser:

```
http://localhost:8501
```

---

# 📸 Screenshots

Application includes:

- Movie search interface
- Movie details page
- Cast information
- Movie recommendation system

*(Add screenshots here later)*

---

# 🔮 Future Improvements

- Add **machine learning based recommendations**
- Implement **watchlists**
- Add **user ratings and reviews**
- Deploy on **Streamlit Cloud**

---

# 📜 License

This project is licensed under the **MIT License**.
