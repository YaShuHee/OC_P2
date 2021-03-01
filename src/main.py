#!/usr/bin/env python3
# coding: utf-8


from functools import cache
import requests
from bs4 import BeautifulSoup


def get_soup(url):
    """
    Returns the html code extracted from the url or an empty string.
    TODO: Recode with exception handling?
    """
    response = requests.get(url)
    if response.ok:
        return BeautifulSoup(response.text, features="html.parser")
    else:
        return ""


@cache
def get_links(soup):
    """
    Returns all the <a> elements from a soup.
    Result is calculated only once for each 'soup' argument given thanks to @cache decorator.
    """
    return soup.findAll("a")


def get_categories(soup):
    """
    Returns a dict containing categories of books as keys and their relative url as values.
    """
    links = get_links(soup)
    return {
        link.contents[0].strip(): "https://books.toscrape.com" + link['href'].replace("index.html", "")
        for link in links if "category/books/" in link["href"]
    }


def get_book_info(url):
    """
    Returns all info from a book, using its url.
    TODO: Coding it.
    """
    return {}


def get_books_url_from_page(soup):
    """
    Returns a list of all the books urls from one page.
    TODO: Coding it.
    """
    return ""


def get_books_from_category(category_url):
    """
    Returns a list of all the books and their infos from one category, using its url.
    """
    pages = 1
    while True:
        break


def main():
    """TODO: """
    soup = get_soup("https://books.toscrape.com")
    categories = get_categories(soup)
    counter = 1
    books = {}
    for category_name, category_url in categories.items():
        print(f"{counter}. {category_name}: {category_url}")
        counter += 1
        # TODO: extract books info from each category
        # books[category_name] = get_books_from_category(category_url)


if __name__ == '__main__':
    main()