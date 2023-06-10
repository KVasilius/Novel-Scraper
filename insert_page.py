import sqlite3
import novel_page_scraper as nps


def insert(url):
    n1 = nps.Novel(url)
    n1.get_details()
    data = n1.novel_data[0]

    cnx = sqlite3.connect('novel_database.db')

    cursor = cnx.cursor()

    if data['novel_title'].replace(" - Novel Updates", "") == "Page not found":
        return

    author_name = data['novel_authors'][0]

    cursor.execute("SELECT author_id FROM authors WHERE author_name = ?", (author_name,))
    row = cursor.fetchone()

    if row is None:
        cursor.execute("INSERT INTO authors (author_name) VALUES (?)", (author_name,))
        author_id = cursor.lastrowid 
    else:
        author_id = row[0]  

    novel_title = data['novel_title'].replace(" - Novel Updates", "")
    novel_description = data['novel_description']
    novel_other_names = ", ".join(data['novel_other_names'])
    novel_related_series = ", ".join(data['novel_related_series'])
    novel_image = data['novel_image']
    novel_type = data['novel_type']
    novel_genre = ", ".join(data['novel_genre'])
    novel_tag_ids = []
    for tag in data['novel_tag']:
        cursor.execute("SELECT tag_id FROM tags WHERE tag_name = ?", (tag,))
        row = cursor.fetchone()
        if not row:
            cursor.execute("INSERT INTO tags (tag_name) VALUES (?)", (tag,))
            tag_id = cursor.lastrowid
        else:
            tag_id = row[0]
        novel_tag_ids.append(tag_id)
    novel_tag_ids = ", ".join(map(str, novel_tag_ids))
    novel_language = data['novel_language']
    novel_authors = ", ".join(data['novel_authors'])
    novel_artists = ", ".join(data['novel_artists'])
    novel_year = data['novel_year']
    novel_original_chapters = ", ".join(data['novel_original_chapters'])
    novel_license = ", ".join(data['novel_license'])
    novel_finished_translation = ", ".join(data['novel_finished_translation'])
    novel_original_publishers = ", ".join(data['novel_original_publishers'])
    novel_english_publishers = ", ".join(data['novel_english_publishers'])
    novel_release_frequency = data['novel_release_frequency']

    cursor.execute('SELECT novel_id FROM novels WHERE novel_title = ?', (novel_title,))
    row = cursor.fetchone()

    if row:
        novel_id = row[0]
        cursor.execute('''
            UPDATE novels SET
            novel_title=?, novel_description=?, novel_other_names=?,
            novel_image=?, novel_type=?, novel_link=?,
            novel_language=?, novel_artists=?, novel_year=?,
            novel_original_chapters=?, novel_license=?, novel_finished_translation=?,
            novel_original_publishers=?, novel_english_publishers=?, novel_release_frequency=?
            WHERE novel_id=?
        ''', (
            novel_title, novel_description, novel_other_names,
            novel_image, novel_type, url,
            novel_language, novel_artists, novel_year,
            novel_original_chapters, novel_license, novel_finished_translation,
            novel_original_publishers, novel_english_publishers, novel_release_frequency,
            novel_id
        ))
    else:
        cursor.execute('''
            INSERT INTO novels (
                novel_id, novel_title, novel_description, novel_other_names,
                novel_image, novel_type, novel_link,
                novel_language, novel_artists, novel_year,
                novel_original_chapters, novel_license, novel_finished_translation,
                novel_original_publishers, novel_english_publishers, novel_release_frequency,
                author_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            None, novel_title, novel_description, novel_other_names,
            novel_image, novel_type, url,
            novel_language, novel_artists, novel_year,
            novel_original_chapters, novel_license, novel_finished_translation,
            novel_original_publishers, novel_english_publishers, novel_release_frequency,
            author_id
        ))

        cursor.execute('SELECT last_insert_rowid()')
        row = cursor.fetchone()
        novel_id = row[0]



    cursor.execute('SELECT novel_id FROM novels WHERE novel_title = ?', (novel_title,))
    row = cursor.fetchone()

    if row:
        novel_id = row[0]
    else:
        novel_id = None
    print(novel_id)

    for series_name in data['novel_related_series']:
        cursor.execute('''
            SELECT series_id FROM related_series WHERE series_name = ? AND novel_id = ?
        ''', (series_name, novel_id))
        row = cursor.fetchone()

        if not row:
            cursor.execute('''
                INSERT INTO related_series (series_name, novel_id) VALUES (?, ?)
            ''', (series_name, novel_id))
        else:
            cursor.execute('''
                SELECT novel_id FROM novels WHERE novel_title = ?
            ''', (series_name,))
            related_row = cursor.fetchone()

            if related_row:
                related_id = related_row[0]
            else:
                related_id = None

            cursor.execute('''
                UPDATE related_series SET related_id = ? WHERE series_name = ? AND novel_id = ?
            ''', (related_id, series_name, novel_id))




    group_ids = {}

    cursor.execute("SELECT group_id, group_name FROM translation_group")
    rows = cursor.fetchall()
    for row in rows:
        group_id, group_name = row
        group_ids[group_name] = group_id

    for tag_id in novel_tag_ids.split(", "):
        cursor.execute('''
            INSERT OR IGNORE INTO novel_tags (novel_id, tag_id) VALUES (?, ?)
        ''', (novel_id, tag_id))

    genres = data['novel_genre']
    for genre in genres:
        cursor.execute("SELECT genre_id FROM genres WHERE genre_name = ?", (genre,))
        row = cursor.fetchone()
        
        if not row:
            cursor.execute("INSERT INTO genres (genre_name) VALUES (?)", (genre,))


    for genre in genres:
        cursor.execute('SELECT genre_id FROM genres WHERE genre_name = ?', (genre,))
        row = cursor.fetchone()

        if not row:
            cursor.execute('INSERT INTO genres (genre_name) VALUES (?)', (genre,))
            genre_id = cursor.lastrowid  
        else:
            genre_id = row[0]  


    for genre in genres:
        cursor.execute('SELECT genre_id FROM genres WHERE genre_name = ?', (genre,))
        row = cursor.fetchone()

        if not row:
            cursor.execute('INSERT INTO genres (genre_name) VALUES (?)', (genre,))
            genre_id = cursor.lastrowid  
        else:
            genre_id = row[0]  

        cursor.execute('''
            SELECT novel_id, genre_id
            FROM novel_genres
            WHERE novel_id = ? AND genre_id = ?
        ''', (novel_id, genre_id))
        row = cursor.fetchone()

        if not row:
            cursor.execute('''
                INSERT INTO novel_genres (novel_id, genre_id)
                VALUES (?, ?)
            ''', (novel_id, genre_id))
        else:
            pass


    for recommendation_name in data['novel_recommendations']:
        if recommendation_name:  
            cursor.execute('''
                SELECT recommendation_id FROM recommendations WHERE recommendation_name = ? AND novel_id = ?
            ''', (recommendation_name, novel_id))
            row = cursor.fetchone()

            if not row:
                cursor.execute('SELECT novel_id FROM novels WHERE novel_title = ?', (recommendation_name,))
                recommended_row = cursor.fetchone()

                if recommended_row:
                    recommended_novel_id = recommended_row[0]
                else:
                    recommended_novel_id = None

                cursor.execute('''
                    INSERT INTO recommendations (recommendation_name, novel_id, recommended_novel_id) VALUES (?, ?, ?)
                ''', (recommendation_name, novel_id, recommended_novel_id))
            else:
                cursor.execute('''
                    SELECT recommended_novel_id FROM recommendations WHERE recommendation_name = ? AND novel_id = ?
                ''', (recommendation_name, novel_id))
                recommended_row = cursor.fetchone()

                if recommended_row[0] is None:
                    cursor.execute('''
                        SELECT novel_id FROM novels WHERE novel_title = ?
                    ''', (recommendation_name,))
                    recommended_row = cursor.fetchone()

                    if recommended_row:
                        recommended_novel_id = recommended_row[0]
                    else:
                        recommended_novel_id = None

                    cursor.execute('''
                        UPDATE recommendations SET recommended_novel_id = ? WHERE recommendation_name = ? AND novel_id = ?
                    ''', (recommended_novel_id, recommendation_name, novel_id))




    for chapter in data['novel_chapter_data']:
        chapter_name = chapter['chapter_name']
        date = chapter['date']
        group_name = chapter['group']
        release = chapter['release']
        chapter_url = chapter['chapter_url']

        if group_name not in group_ids:
            cursor.execute("INSERT INTO translation_group (group_name) VALUES (?)", (group_name,))
            group_id = cursor.lastrowid  
            group_ids[group_name] = group_id
        else:
            group_id = group_ids[group_name]  

        cursor.execute('''
            SELECT chapter_id FROM chapters WHERE chapter_name = ? AND novel_id = ?
        ''', (chapter_name, novel_id))
        row = cursor.fetchone()

        if not row:
            cursor.execute('''
                INSERT INTO chapters (chapter_name, date, release, chapter_url, novel_id, group_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (chapter_name, date, release, chapter_url, novel_id, group_id))


    cnx.commit()
    cursor.close()
    cnx.close()

#insert("https://www.novelupdates.com/series/hack-aibuster/")