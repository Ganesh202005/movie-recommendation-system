import sqlite3
import streamlit as st
import requests
import qrcode
import os
import uuid
import time
import datetime
import base64
from streamlit_autorefresh import st_autorefresh

# --- CONFIGURATION ---
movie_title = "Piku"
movie_path = r"D:\MOVIES\Piku 2015 Hindi 720p BluRay 900MB [BollyFlix].mkv"
api_url = "https://script.google.com/macros/s/AKfycbz6qaJBinOiay49d8yedaK4i_aR2z9ceNZMagJbFbrtBRhoT6uIaYVR7Nrxas74Sl4/exec?order_id="  # Replace with your actual API
qr_code_path = "assets/qr/qr_ea9c6975.png"  # Replace with your actual QR image path or URL

# --- DATABASE FUNCTION ---
def add_movie(title, video_path):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        video_path TEXT NOT NULL
    )
    ''')
    cursor.execute("INSERT INTO movies (title, video_path) VALUES (?, ?)", (title, video_path))
    conn.commit()
    conn.close()

def generate_qr_code(data, save_dir='assets/qr'):
    # Ensure the save directory exists
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Generate a unique filename
    filename = f"qr_{uuid.uuid4().hex[:8]}.png"
    full_path = os.path.join(save_dir, filename)

    # Create the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Save the image
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(full_path)

    return full_path


def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# --- STREAMLIT UI ---
st.set_page_config(page_title="Movie Purchase System", layout="centered")
st.title("Welcome to the Movie Purchase System")
st.write(f"Movie Title: {movie_title}")

# --- Session state initialization ---
# Initialize polling timestamp in session state
if "last_poll_time" not in st.session_state:
    st.session_state.last_poll_time = 0
if "show_popup" not in st.session_state:
    st.session_state.show_popup = False
if "transaction_complete" not in st.session_state:
    st.session_state.transaction_complete = False

# --- Sidebar Purchase Button ---
if "order_id" not in st.session_state:
    st.session_state.order_id = None
if "qr_code_path" not in st.session_state:
    st.session_state.qr_code_path = None

amount = 1.00

if st.sidebar.button("Purchase Movie"):
    st.session_state.show_popup = True
    st.session_state.transaction_complete = False
    st.session_state.order_id = int(time.time())
    qr_data = f"upi://pay?pa=paytmqr5lwrim@ptys&pn=RAJDIP%20CHANDRAKANT%20PATIL&am={amount}&tr={st.session_state.order_id}&tn=taxi%20bill"
    st.session_state.qr_code_path = generate_qr_code(qr_data)
    st_autorefresh(interval=2000, limit=None, key="poll_qr")


# --- POLLING LOGIC ---
# --- POLLING LOGIC (Correct way for Streamlit) ---
if st.session_state.show_popup and not st.session_state.transaction_complete:
    current_time = time.time()

    # Poll only every 2 seconds
    if current_time - st.session_state.last_poll_time > 2:
        st.session_state.last_poll_time = current_time

        try:
            response = requests.get(api_url + str(st.session_state.order_id))
            data = response.json()
            if data.get("code") == 200:
                st.session_state.transaction_complete = True
                st.session_state.show_popup = False
                add_movie(movie_title, movie_path)
                st.sidebar.success(f"✅ Successfully purchased and added '{movie_title}' to the database!")
            else:
                st.info("🔄 Waiting for payment confirmation...")
        except Exception as e:
            st.warning(f"Error while checking payment status: {e}")

    # Auto-refresh to re-run after short interval
    st_autorefresh(interval=2000, limit=None, key="poll_qr")

# --- POPUP UI ---
# Inside your popup rendering
if st.session_state.show_popup:
    base64_qr = get_base64_image(st.session_state.qr_code_path)
    st.markdown(f"""
        <div style="position:fixed; top:0; left:0; width:100%; height:100%; background-color:rgba(0,0,0,0.6); display:flex; align-items:center; justify-content:center; z-index:9999;">
            <div style="background:white; padding:30px; border-radius:10px; text-align:center;">
                <h3>Scan QR to Complete Payment</h3>
                <img src="data:image/png;base64,{base64_qr}" width="200"><br><br>
                <div class="loader"></div>
                <p>Waiting for payment confirmation...</p>
            </div>
        </div>

        <style>
        .loader {{
            border: 6px solid #f3f3f3;
            border-top: 6px solid #3498db;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: auto;
        }}

        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        </style>
    """, unsafe_allow_html=True)


# --- Play Movie ---
if st.button("Play Movie"):
    st.video(movie_path)
