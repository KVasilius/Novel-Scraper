import cloudscraper
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_data(url):
    soup = BeautifulSoup(cloudscraper.create_scraper().get(url).content, "lxml")
    elements = soup.find_all('div', class_='search_main_box_nu')

    data = []
    for element in elements:
        title_element = element.find('div', class_='search_title').find('a')
        title = title_element.text.strip()
        link = urljoin(url, title_element['href'])  

        image = element.find('img')['src']

        data.append({
            "novel_title": title,
            "novel_link": link,  
            "novel_image": image
        })

    return data

def get_next_page_url(soup, base_url):
    next_page_link = soup.find('a', class_='next_page')
    if next_page_link:
        next_page_url = urljoin(base_url, next_page_link['href'])
        return next_page_url
    else:
        return None

def scrape_multiple_pages(base_url):
    all_data = []

    url = base_url
    while url:
        soup = BeautifulSoup(cloudscraper.create_scraper().get(url).content, "lxml")
        data = scrape_data(url)
        all_data.extend(data)
        url = get_next_page_url(soup, base_url)
    return all_data

