Movie Recommendation & Purchase System
This is a full-stack Streamlit web application for movie recommendations powered by The Movie Database (TMDb) API, integrated with a QR-based payment system for purchasing and unlocking movies.

Built by a BCA student from Mumbai passionate about film production, screenwriting, and tech projects.
​

Features
User authentication with login/signup screen.
​

Search movies by name, fetch details (poster, overview, IMDb rating, trailer, cast).
​

View top 5 cast members with expandable actor bios.
​

Get personalized recommendations based on selected movie.
​

Sidebar navigation for Bollywood/Hollywood streams and purchase pages.
​

QR code generation for UPI payments (e.g., Paytm) with real-time polling for confirmation.

SQLite database to store purchased movies; play unlocked videos post-payment.
​

Auto-refresh and responsive UI with custom CSS styling.

File Structure
File	Description
main.py	Core app: login, search, recommendations, TMDb integration, sidebar menu.
​
page.py	Movie purchase page: QR popup, payment polling, video unlock.
​
qr.py	QR code generator for payment links.
​
payment.py	Payment status verification with retry logic.
​
Note: Additional files like login.py, bollywood.py referenced but not attached.
​

Tech Stack
Frontend/Backend: Streamlit

APIs: TMDb (movies, cast, trailers), Google Apps Script (payment verify)

Database: SQLite

Payments: UPI QR (Paytm)

Libraries: requests, qrcode[pil], streamlit-autorefresh, base64

Quick Setup
Clone repo and install dependencies:

text
pip install streamlit requests qrcode[pil] streamlit-autorefresh
Get TMDb API key from themoviedb.org and replace in main.py.
​

Update payment API URL in page.py (e.g., your Google Script endpoint).
​

Run the app:

text
streamlit run main.py
Access at http://localhost:8501. Login, search movies, purchase via QR.

API Keys & Config
TMDb: Replace 93a7261b8594ec9d691f6bd21a977afc in main.py.
​

Payment: Update apiurl in page.py; test with your endpoint returning {"code": 200} on success.
​

Screenshots
Demo shows movie search, details, cast, recommendations, and QR payment popup.

Future Plans
Integrate full Bollywood/Hollywood catalogs.

Add user watchlists and ratings.

Deploy to Streamlit Cloud/Hugging Face Spaces.

Enhance with ML-based recommendations.

Contributing
Fork, PR improvements! Focus on security, error handling, or new features like subscriptions.
​

License
MIT License. Free to use/modify.
