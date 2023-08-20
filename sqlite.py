# Generates the sqlite tables (users, televisions, tests) and inserts some records for demonstration purposes

import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create the 'users' table
# Stores admin/regular users' usernames and passwords
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        approved INTEGER DEFAULT 0,
        user_type TEXT NOT NULL
    )
''')

# Username: admin
# Password: Pass123?

# Inserting a (pre-made) Admin record to login with.
user_data = {'username': 'admin', 'password': 'Pass123?', 'user_type': 'admin', 'approved': 1}
c.execute('''INSERT INTO users(username, password, user_type, approved) VALUES (?, ?, ?, ?)''',
          (user_data['username'], user_data['password'], user_data['user_type'], user_data['approved']))

# Create the 'Televisions' table
# Stores a list of Television records for engineers to view television specifications
c.execute('''
    CREATE TABLE IF NOT EXISTS Televisions (
        tv_id INTEGER PRIMARY KEY AUTOINCREMENT,
        brand TEXT NOT NULL,
        audio TEXT NOT NULL,
        resolution TEXT NOT NULL,
        refresh_rate TEXT NOT NULL,
        screen_size TEXT NOT NULL
    )
''')
          
# Create the 'Tests' table
# Stores a list of Test records for engineers to view test cases and their configuration
c.execute('''
    CREATE TABLE IF NOT EXISTS Tests (
        test_id INTEGER PRIMARY KEY AUTOINCREMENT,
        test_name TEXT NOT NULL,
        duration DECIMAL(5, 2) NOT NULL,
        region TEXT NOT NULL,
        audio_test_type TEXT,
        playback_type TEXT,
        test_criteria TEXT,
        test_parameters TEXT
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
