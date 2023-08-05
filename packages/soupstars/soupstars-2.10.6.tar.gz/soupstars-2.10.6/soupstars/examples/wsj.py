from soupstars import data

url = "https://wsj.com"


@data
def headlines(soup):
    results = []
    for article in soup.find_all('article'):
        text = article.find('a').text
        if len(text) > 5:
            results.append(text)
    return results
