#!/usr/bin/env python3
# coding: utf-8


import requests
from bs4 import BeautifulSoup


def get_soup(url):
    response = requests.get(url)
    if response.ok:
        return BeautifulSoup(response.text)
    else:
        return ""


def get_links(soup):
    return soup.findAll("a")


def get_categories(soup):
    links = get_links(soup)
    return [
        link['href'].removeprefix("catalogue/category/books/").removesuffix("/index.html")
        for link in links if "category/books/" in link["href"]
    ]


def main():
    soup = get_soup("https://books.toscrape.com")
    categories = get_categories(soup)
    counter = 1
    for category in categories:
        print(f"{counter}. {category}")
        counter += 1


if __name__ == '__main__':
    main()