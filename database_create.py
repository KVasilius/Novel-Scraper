import sqlite3

def create_database():
    
    cnx = sqlite3.connect('novel_database.db')
    cursor = cnx.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS authors (
            author_id INTEGER PRIMARY KEY AUTOINCREMENT,
            author_name VARCHAR(100) NOT NULL
        )
    ''')


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tags (
            tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag_name VARCHAR(50) NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS novels (
            novel_id INTEGER PRIMARY KEY AUTOINCREMENT,
            novel_title VARCHAR(100) NOT NULL,
            novel_link TEXT,
            novel_description TEXT,
            novel_other_names TEXT,
            novel_image TEXT,
            novel_type VARCHAR(50),
            novel_language VARCHAR(50),
            novel_artists TEXT,
            novel_year VARCHAR(10),
            novel_original_chapters TEXT,
            novel_license TEXT,
            novel_finished_translation TEXT,
            novel_original_publishers TEXT,
            novel_english_publishers TEXT,
            novel_release_frequency TEXT,
            author_id INT,
            FOREIGN KEY (author_id) REFERENCES authors(author_id) ON DELETE CASCADE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS novel_tags (
            novel_id INT,
            tag_id INT,
            PRIMARY KEY (novel_id, tag_id),
            FOREIGN KEY (novel_id) REFERENCES novels(novel_id) ON DELETE CASCADE,
            FOREIGN KEY (tag_id) REFERENCES tags(tag_id) ON DELETE CASCADE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS related_series (
            series_id INTEGER PRIMARY KEY AUTOINCREMENT,
            series_name VARCHAR(100) NOT NULL,
            novel_id INT,
            related_id INT,
            FOREIGN KEY (novel_id) REFERENCES novels(novel_id) ON DELETE CASCADE,
            FOREIGN KEY (related_id) REFERENCES novels(novel_id) ON DELETE SET NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recommendations (
            recommendation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            recommendation_name VARCHAR(100) NOT NULL,
            novel_id INT,
            recommended_novel_id INT,
            FOREIGN KEY (novel_id) REFERENCES novels(novel_id) ON DELETE CASCADE,
            FOREIGN KEY (recommended_novel_id) REFERENCES novels(novel_id) ON DELETE SET NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS genres (
        genre_id INTEGER PRIMARY KEY,
        genre_name TEXT UNIQUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS novel_genres (
            novel_id INT,
            genre_id INT,
            PRIMARY KEY (novel_id, genre_id),
            FOREIGN KEY (novel_id) REFERENCES novels(novel_id) ON DELETE CASCADE,
            FOREIGN KEY (genre_id) REFERENCES genres(genre_id) ON DELETE CASCADE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS translation_group (
            group_id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_name VARCHAR(100) NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chapters (
            chapter_id INTEGER PRIMARY KEY AUTOINCREMENT,
            chapter_name VARCHAR(100) NOT NULL,
            date DATE,
            release VARCHAR(100),
            chapter_url VARCHAR(200),
            novel_id INT,
            group_id INT,
            FOREIGN KEY (novel_id) REFERENCES novels(novel_id) ON DELETE CASCADE,
            FOREIGN KEY (group_id) REFERENCES translation_group(group_id) ON DELETE CASCADE
        )
    ''')

    cnx.commit()
    cursor.close()
    cnx.close()