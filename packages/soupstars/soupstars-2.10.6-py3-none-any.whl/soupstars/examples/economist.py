"""
Extract metadata from economist index and article pages

"""

import dateparser

from soupstars import data


@data
def date(soup):
    "The date of the article"

    string = soup.find(attrs={'class': 'print-edition__main-title-header__date'})  # noqa
    text = string.text.strip()
    return dateparser.parse(text).date()


@data
def articles(soup):
    "The paths of the article urls"

    spans = soup.find_all('span', attrs={'class': 'print-edition__link-title'})
    return [span.parent['href'] for span in spans]


@data
def num_articles(soup):
    "The number of articles found on the page"

    return len(articles(soup))
