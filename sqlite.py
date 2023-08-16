import sqlite3

conn = sqlite3.connect('sea-assignment/database.db')
c = conn.cursor()

# Create the 'users' table
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        approved INTEGER DEFAULT 0,
        user_type TEXT NOT NULL
    )
''')

# Insert the admin user record
user_data = {'username': 'admin', 'password': '123', 'user_type': 'admin', 'approved': 1}
c.execute('''INSERT INTO users(username, password, user_type, approved) VALUES (?, ?, ?, ?)'''
          , (user_data['username'], user_data['password'], user_data['user_type'], user_data['approved']))

# Create the 'Televisions' table
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

# Create the 'Television Tests' table    
c.execute('''
    CREATE TABLE IF NOT EXISTS Television_Tests (
        television_test_id INTEGER PRIMARY KEY,
        tv_id INTEGER NOT NULL,
        test_id INTEGER NOT NULL,
        FOREIGN KEY (tv_id) REFERENCES Televisions(tv_id),
        FOREIGN KEY (test_id) REFERENCES Tests(test_id)
    )
''')
          
# Insert Television records
c.execute('''
    INSERT INTO Televisions (tv_id, brand, audio, resolution, refresh_rate, screen_size)
    VALUES
        (1, 'Samsung', '95W', '8K', '144Hz', '70in'),
        (2, 'Samsung', '85W', '4K', '120Hz', '55in'),
        (3, 'Samsung', '110W', '4K', '60Hz', '65in'),
        (4, 'Sony', '120W', '4K', '120Hz', '65in'),
        (5, 'Sony', '110W', '8K', '144Hz', '75in'),
        (6, 'Sony', '90W', '4K', '60Hz', '55in'),
        (7, 'LG', '80W', '4K', '60Hz', '55in'),
        (8, 'LG', '100W', '8K', '120Hz', '65in'),
        (9, 'LG', '70W', '4K', '120Hz', '75in');
''')

          
# Insert Tests records
c.execute('''
    INSERT INTO Tests (test_id, test_name, duration, region, audio_test_type, playback_type, test_criteria, test_parameters)
    VALUES
        (1, 'Audio Quality Test', 15.5, 'North America', 'Audio Quality', 'Music Playback', 'Signal-to-Noise Ratio > 80dB', 'Lossless audio format'),
        (2, 'Video Playback Test', 30.0, 'Europe', 'Playback Quality', 'Video Playback', 'No Frame Drops', 'HD resolution'),
        (3, 'Surround Sound Test', 25.0, 'Asia', 'Surround Sound Quality', 'Movie Playback', 'All Speakers Audible', 'Dolby Atmos configuration'),
        (4, 'Bass Performance Test', 10.0, 'North America', 'Audio Quality', 'Music Playback', 'Deep Bass Audibility', 'Subwoofer connected'),
        (5, 'Audio Balance Test', 12.0, 'Europe', 'Audio Balance', 'Music Playback', 'Balanced Left/Right Audio', 'Stereo audio source'),
        (6, 'Color Accuracy Test', 20.0, 'Asia', 'Color Accuracy', 'Video Playback', 'Delta E < 3', 'Color calibration enabled'),
        (7, 'HDR Playback Test', 22.5, 'North America', 'HDR Playback', 'Video Playback', 'HDR Content Rendering', 'HDR10 format'),
        (8, 'Motion Smoothness Test', 18.0, 'Europe', 'Motion Smoothness', 'Video Playback', 'No Judder or Blur', '120Hz refresh rate'),
        (9, 'Voice Clarity Test', 8.5, 'Asia', 'Audio Quality', 'Voice Playback', 'Clear Dialog Audibility', 'Voice enhancement mode'),
        (10, 'Gaming Performance Test', 24.0, 'North America', 'Gaming Performance', 'Gaming Playback', 'Low Input Lag', 'Game Mode enabled');
''')
          
# Insert Television Tests mapping
c.execute('''
    INSERT INTO Television_Tests (tv_id, test_id)
    VALUES
        (8, 1),    -- Samsung TV linked with Audio Quality Test
        (11, 1),   -- Samsung TV linked with Audio Quality Test
        (12, 1),   -- Samsung TV linked with Audio Quality Test
        (13, 1),   -- Samsung TV linked with Audio Quality Test
        (14, 2),   -- Sony TV linked with Video Playback Test
        (15, 2),   -- Sony TV linked with Video Playback Test
        (16, 2),   -- Sony TV linked with Video Playback Test
        (17, 3),   -- LG TV linked with Surround Sound Test
        (18, 3),   -- LG TV linked with Surround Sound Test
        (19, 3);   -- LG TV linked with Surround Sound Test
''')


conn.commit()
conn.close()
