# Generates the sqlite tables (users, televisions, tests) and inserts some records for demonstration purposes

import sqlite3
from helpers import hash_password

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create the 'users' table
# Stores admin/regular users' usernames and passwords
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL CHECK(length(username) <= 50),
        password TEXT NOT NULL,
        is_admin INTEGER DEFAULT 0,
        UNIQUE(username)
    )
''')

# Username: admin
# Password: Pass123?

# Inserting a (pre-made) Admin record to login with.
user_data = {'username': 'admin', 'password': hash_password("Pass123?"), 'is_admin': 1}
c.execute('''INSERT INTO users(username, password, is_admin) VALUES (?, ?, ?)''',
          (user_data['username'], user_data['password'], user_data['is_admin']))

# Create the 'Televisions' table
# Stores a list of Television records for engineers to view television specifications
c.execute('''
    CREATE TABLE IF NOT EXISTS Televisions (
        tv_id INTEGER PRIMARY KEY AUTOINCREMENT,
        brand TEXT NOT NULL CHECK(length(brand) <= 50),
        audio TEXT NOT NULL CHECK(length(audio) <= 50),
        resolution TEXT NOT NULL CHECK(length(resolution) <= 50),
        refresh_rate TEXT NOT NULL CHECK(length(refresh_rate) <= 50),
        screen_size TEXT NOT NULL CHECK(length(screen_size) <= 50)
    )
''')
          
# Create the 'Tests' table
# Stores a list of Test records for engineers to view test cases and their configuration
c.execute('''
    CREATE TABLE IF NOT EXISTS Tests (
        test_id INTEGER PRIMARY KEY AUTOINCREMENT,
        test_name TEXT NOT NULL CHECK(length(test_name) <= 50),
        duration DECIMAL(5, 2) NOT NULL,
        region TEXT NOT NULL CHECK(length(region) <= 50),
        audio_test_type TEXT CHECK(length(audio_test_type) <= 50),
        playback_type TEXT CHECK(length(playback_type) <= 50), 
        test_criteria TEXT CHECK(length(test_criteria) <= 100),
        test_parameters TEXT CHECK(length(test_parameters) <= 100),
        author_id INTEGER,
        FOREIGN KEY (author_id) REFERENCES users(id)
    )
''')
          
# Insert 10 Television records
tv_records = [
    (1, 'Samsung', '95W', '8K', '144Hz', '70in'),
    (2, 'Samsung', '85W', '4K', '120Hz', '55in'),
    (3, 'Samsung', '110W', 'HD', '60Hz', '75in'),
    (4, 'Sony', '120W', '4K', '120Hz', '65in'),
    (5, 'Sony', '110W', '8K', '144Hz', '75in'),
    (6, 'Sony', '90W', '4K', '60Hz', '55in'),
    (7, 'LG', '80W', '4K', '60Hz', '55in'),
    (8, 'LG', '100W', '8K', '120Hz', '65in'),
    (9, 'LG', '70W', '4K', '120Hz', '75in'),
    (10, 'LG', '100W', 'HD', '120Hz', '75in')
]
for record in tv_records:
    c.execute('''
        INSERT INTO Televisions (tv_id, brand, audio, resolution, refresh_rate, screen_size)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', record)


# Insert 10 Tests cases
test_records = [
    (1, 'Audio Quality Test', 15.5, 'North America', 'Audio Quality', 'Audio Playback', '95W to 100W', 'Lossless format'),
    (2, 'Video Playback Test', 30.0, 'Europe', 'Playback Quality', 'Video Playback', '4K', 'HD resolution'),
    (3, 'Surround Sound Test', 25.0, 'Asia', 'Surround Sound Quality', 'Video Playback', 'HD', 'Speaker configuration'),
    (4, 'Bass Performance Test', 10.0, 'North America', 'Audio Quality', 'Audio Playback', '80W to 120 W', 'Subwoofer connected'),
    (5, 'Audio Balance Test', 12.0, 'Europe', 'Audio Balance', 'Audio Playback', '80W to 120 W', 'Stereo audio source'),
    (6, 'Color Accuracy Test', 20.0, 'Asia', 'Color Accuracy', 'Video Playback', 'HD', 'Color calibration enabled'),
    (7, 'HDR Playback Test', 22.5, 'North America', 'HDR Playback', 'Video Playback', 'HD', 'HDR10 format'),
    (8, 'Motion Smoothness Test', 18.0, 'Europe', 'Motion Smoothness', 'Video Playback', '4K', '120Hz refresh rate'),
    (9, 'Voice Clarity Test', 8.5, 'Asia', 'Audio Quality', 'Voice Playback', '95W to 100W', 'Voice enhancement mode'),
    (10, 'Gaming Performance Test', 24.0, 'North America', 'Gaming Performance', 'HD or 4K', 'Low Latency', 'Game Mode on')
]

for record in test_records:
    c.execute('''
        INSERT INTO Tests (test_id, test_name, duration, region, audio_test_type, playback_type, test_criteria, test_parameters)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', record)

conn.commit()
conn.close()
