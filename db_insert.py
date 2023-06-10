import sqlite3
import novel_database_scraper as nds


def database_scrape(url):
    novel_data_list = nds.scrape_multiple_pages(url)

    cnx = sqlite3.connect('novel_database.db')

    cursor = cnx.cursor()

    for data in novel_data_list:
        novel_title = data['novel_title'].replace(" - Novel Updates", "")
        novel_image = data['novel_image']
        novel_link = data['novel_link']

        cursor.execute('SELECT novel_id FROM novels WHERE novel_title = ?', (novel_title,))
        row = cursor.fetchone()

        if not row:
            cursor.execute('''
                INSERT INTO novels (
                    novel_id, novel_title, novel_image, novel_link
                )
                VALUES (?, ?, ?, ?)
            ''', (
                None, novel_title, novel_image, novel_link
            ))

    cnx.commit()
    cursor.close()
    cnx.close()
    return
