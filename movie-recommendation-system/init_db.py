import sqlite3

# Connect to the database (will create if it doesn't exist)
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create the movies table
cursor.execute('''
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    video_path TEXT NOT NULL
)
''')

# Add Piku movie (make sure the path below is correct)
cursor.execute("INSERT INTO movies (title, video_path) VALUES (?, ?)",
               ("Piku", r"D:\MOVIES\Piku 2015 Hindi 720p BluRay 900MB [BollyFlix].mkv"))

# Save changes and close
conn.commit()
conn.close()
