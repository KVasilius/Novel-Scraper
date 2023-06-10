import cloudscraper
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class Novel:
    def __init__(self, url):
        self.soup = BeautifulSoup(cloudscraper.create_scraper().get(url).content, "lxml")
        self.url = url
        self.novel_title = ""
        self.novel_description = ""
        self.novel_other_names = []
        self.novel_related_series = []
        self.novel_recommendations = []
        self.novel_chapter_data = []
        self.novel_image = ""
        self.novel_type = ""
        self.novel_genre = []
        self.novel_tag = []
        self.novel_language = ""
        self.novel_authors = []
        self.novel_artists = []
        self.novel_year = ""
        self.novel_original_chapters = []
        self.novel_license = []
        self.novel_finished_translation = []
        self.novel_original_publishers = []
        self.novel_english_publishers = []
        self.novel_release_frequency = ""
        self.novel_data = []

    def get_details(self):
        self.get_novel_title()
        self.get_mid_details()
        self.get_left_details()
        self.get_chapters()
        self.output()

    def get_novel_title(self):
        title_tag = self.soup.find("title")
        if title_tag:
            self.novel_title = title_tag.get_text(strip=True)

    def get_mid_details(self):
        description_element = self.soup.find("div", id="editdescription")
        if description_element:
            self.novel_description = description_element.get_text(strip=True)

        other_names_div = self.soup.find("div", id="editassociated")
        if other_names_div:
            self.novel_other_names = [name.strip() for name in other_names_div.stripped_strings]

        related_series_div = self.soup.find("h5", text="Related Series")
        if related_series_div:
            for sibling in related_series_div.find_next_siblings():
                if sibling.name == "h5":
                    break
                self.novel_related_series.append(sibling.text.strip())

        recommendations_div = self.soup.find("h5", text="Recommendations")
        if recommendations_div:
            for sibling in recommendations_div.find_next_siblings():
                if sibling.name == "h5":
                    break
                self.novel_recommendations.append(sibling.text.strip())

    def get_left_details(self):
        image_element = self.soup.select_one("div.seriesimg img")
        if image_element:
            self.novel_image = image_element["src"]
        else:
            self.novel_image = ""
        
        type_element = self.soup.select_one("div#showtype a")
        if type_element:
            self.novel_type = type_element.text.strip()
        else:
            self.novel_type = ""
        
        genre_div = self.soup.find("div", id="seriesgenre")
        if genre_div:
            self.novel_genre = [genre.text.strip() for genre in genre_div.find_all("a")]
        else:
            self.novel_genre = []
        
        tag_div = self.soup.find("div", id="showtags")
        if tag_div:
            self.novel_tag = [tag.text.strip() for tag in tag_div.find_all("a")]
        else:
            self.novel_tag = []

        language_element = self.soup.select_one("div#showlang a")
        if language_element:
            self.novel_language = language_element.text.strip()
        else:
            self.novel_language = ""

        self.novel_authors = [author.text.strip() for author in self.soup.select("div#showauthors a")]

        self.novel_artists = [artist.text.strip() for artist in self.soup.select("div#showartists a")]

        year_element = self.soup.select_one("div#edityear")
        if year_element:
            self.novel_year = year_element.text.strip()
        else:
            self.novel_year = ""

        for index in self.soup.select("div#editstatus"):
            self.novel_original_chapters = index.get_text(strip=True).split(",")

        self.novel_license = [license.text.strip() for license in self.soup.select("div#showlicensed")]

        self.novel_finished_translation = [translation.text.strip() for translation in self.soup.select("div#showtranslated")]

        self.novel_original_publishers = [publisher.text.strip() for publisher in self.soup.select("div#showopublisher a")]

        self.novel_english_publishers = [publisher.text.strip() for publisher in self.soup.select("div#showepublisher a")]

        release_frequency_elements = self.soup.select("div#releasestatus div.sSpacing")
        self.novel_release_frequency = release_frequency_elements[0].text.strip() if release_frequency_elements else "N/A"

    def get_chapters(self):
        chapter_table = self.soup.find("table", id="myTable")

        if chapter_table:
            chapter_rows = chapter_table.find_all("tr")

            for row in chapter_rows:
                cells = row.find_all("td")

                if len(cells) == 3:
                    date_cell, group_cell, release_cell = cells

                    date = date_cell.text.strip()
                    group = group_cell.text.strip()

                    if release_cell.a:
                        release = release_cell.a.get("title", "").strip()
                        chapter_url = release_cell.a["href"].strip()
                        chapter_name = release_cell.a.text.strip()

                        self.novel_chapter_data.append({
                            "date": date,
                            "group": group,
                            "release": release,
                            "chapter_url": chapter_url,
                            "chapter_name": chapter_name
                        })

        pagination_div = self.soup.find("div", class_="digg_pagination")
        next_page_link = None
        if pagination_div:
            next_page_link = pagination_div.find("a", class_="next_page")

        if next_page_link:
            next_page_url = next_page_link["href"]
            next_page_full_url = urljoin(self.url, next_page_url)
            self.soup = BeautifulSoup(cloudscraper.create_scraper().get(next_page_full_url).content, "lxml")
            self.get_chapters()


    def output(self):

        self.novel_data.append({
            "novel_title": self.novel_title,
            "novel_description": self.novel_description,
            "novel_other_names": self.novel_other_names,
            "novel_related_series": self.novel_related_series,
            "novel_recommendations": self.novel_recommendations,
            "novel_image": self.novel_image,
            "novel_type": self.novel_type,
            "novel_genre": self.novel_genre,
            "novel_tag": self.novel_tag,
            "novel_language": self.novel_language,
            "novel_authors": self.novel_authors,
            "novel_artists": self.novel_artists,
            "novel_year": self.novel_year,
            "novel_original_chapters": self.novel_original_chapters,
            "novel_license": self.novel_license,
            "novel_finished_translation": self.novel_finished_translation,
            "novel_original_publishers": self.novel_original_publishers,
            "novel_english_publishers": self.novel_english_publishers,
            "novel_release_frequency": self.novel_release_frequency,
            "novel_chapter_data": self.novel_chapter_data
        })


# n1 = Novel("https://www.novelupdates.com/series/overlord/")
# n1.get_details()
# n1.output()
# n1.get_chapters()
# for data in n1.novel_data:
#     print(f"Title: {data['novel_title']}")
#     print(f"Novel Description: {data['novel_description']}")
#     print(f"Other Names: {data['novel_other_names']}")
#     print(f"Related Series: {data['novel_related_series']}")
#     print(f"Recommendations: {data['novel_recommendations']}")
#     print(f"Image: {data['novel_image']}")
#     print(f"Type: {data['novel_type']}")
#     print(f"Genre: {data['novel_genre']}")
#     print(f"Tag: {data['novel_tag']}")
#     print(f"Language: {data['novel_language']}")
#     print(f"Authors: {data['novel_authors']}")
#     print(f"Artists: {data['novel_artists']}")
#     print(f"Year: {data['novel_year']}")
#     print(f"Original Chapters: {data['novel_original_chapters']}")
#     print(f"License: {data['novel_license']}")
#     print(f"Finished Translation: {data['novel_finished_translation']}")
#     print(f"Original Publishers: {data['novel_original_publishers']}")
#     print(f"English Publishers: {data['novel_english_publishers']}")
#     print(f"Release Frequency: {data['novel_release_frequency']}")
#     print()
#     for chapter in data['novel_chapter_data']:
#         print("Chapter Name:", chapter["chapter_name"])
#         print("Date:", chapter["date"])
#         print("Group:", chapter["group"])
#         print("Release:", chapter["release"])
#         print("Chapter URL:", chapter["chapter_url"])
#         print()