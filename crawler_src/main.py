import requests
from bs4 import BeautifulSoup


def get_page(url):
    try:
        res = requests.get(url)
    except:
        return None
    print(res.status_code)
    return res


def find_links(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup.find_all('a')


if __name__ == "__main__":
    link = "https://paris.craigslist.org/search/hhh?lang=en&cc=gb"
    response = get_page(link)
    links = find_links(response.text)
    for link in links:
        print(link.get('href'))
