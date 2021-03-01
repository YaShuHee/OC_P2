#!/usr/bin/env python3
# coding: utf-8


from functools import cache
import requests
from bs4 import BeautifulSoup

import os
cwd = os.getcwd()
results_dir_name = "scraping_results"

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
    return soup.find_all("a")


def get_categories(soup):
    """
    Returns a dict containing categories of books as keys and their relative url as values.
    """
    links = get_links(soup)
    return {
        link.contents[0].strip(): "https://books.toscrape.com/" + link['href'].replace("index.html", "")
        for link in links if "category/books/" in link["href"]
    }


def get_books_infos_from_category(category, category_url):
    """
    Returns a list of all the books and their infos from one category, using its url.
    """
    page = 1
    books = []
    while True:
        if page == 1:
            url_ending = "index.html"
        else:
            url_ending = f"page-{page}.html"
        page_soup = get_soup(category_url + url_ending)
        if page_soup == "":
            print(f"/{page-1}\n")
            break
        else:
            books_urls = get_books_url_from_page(page_soup)
            for book_url in books_urls:
                books.append(get_book_infos(category, book_url))
        print(f"[CAT.] {category} - page {page}", end="")
        page += 1
    return books


def get_books_url_from_page(soup):
    """
    Returns a list of all the books urls from one page.
    TODO: Coding it.
    """
    imgs = soup.find_all("img")
    urls = ["https://books.toscrape.com/catalogue/" + img.parent["href"].replace("../", "") for img in imgs]
    return urls


def scrap_book_informations_table(soup):
    """
    Returns the infos in the "Product Information" table, in a dict.
    """
    table_rows = soup.find_all("tr")
    infos = {
        row.th.text: row.td.text
        for row in table_rows
    }
    return infos


def clean_up_book_informations_table(infos):
    """
    Changes the keys in the dict reported by the function 'scrap_book_informations_table(soup)'.
    """
    cleaned_up_infos = {
        "universal_product_code": infos["UPC"],
        "price_including_tax": infos["Price (incl. tax)"][2:],
        "price_excluding_tax": infos["Price (excl. tax)"][2:],
        "number_available": infos["Availability"].replace("In stock (", "").replace(" available)", "")
    }
    return cleaned_up_infos


def scrap_book_description(soup):
    """
    Returns the book description in a dict.
    """
    try:
        description = soup.find("div", {"id": "product_description"}).find_next_sibling("p").text
    except:
        description = "Pas de description."
        print(f"<!> Pas de description : {scrap_book_title(soup)['title']} <!>")
    return {"product_description": description}


def scrap_book_title(soup):
    """
    Returns the book title in a dict.
    """
    return {"title": soup.find("h1").text}


def number_word_to_number_digits(word):
    return {
        "One": "1",
        "Two": "2",
        "Three": "3",
        "Four": "4",
        "Five": "5"
    }[word]


def scrap_book_review_rating(soup):
    """
    Returns the book review rating in a dict.
    """
    stars = soup.find("div", class_="product_main").find("p", class_="star-rating")["class"][1]
    return {"review_rating": number_word_to_number_digits(stars)}


def scrap_book_image_url(soup):
    """
    Returns the book image url in a dict.
    """
    image_url = "https://books.toscrape.com/catalogue/" + soup.find("article", class_="product_page").find("img")["src"].replace("../", "")
    return {"image_url": image_url}


def get_book_infos(category, url):
    """
    Returns all info from a book, using its url.
    TODO: Coding it.
    """
    infos = {"category": category, "product_page_url": url}
    soup = get_soup(url)
    table_infos = clean_up_book_informations_table(scrap_book_informations_table(soup))
    description_dict = scrap_book_description(soup)
    title_dict = scrap_book_title(soup)
    image_dict = scrap_book_image_url(soup)
    rating_dict = scrap_book_review_rating(soup)

    infos = {
        **infos,
        **table_infos,
        **description_dict,
        **title_dict,
        **rating_dict,
        **image_dict
    }

    print(f" - {infos['title']}")
    return infos


def generate_csv(category_name, books, separator=";"):
    with open(f"{cwd}{os.sep}book_scraping_results_OC_P2{os.sep}{results_dir_name}.csv", "w") as file:
        to_write = ""
        columns =(
                "product_page_url",
                "universal_product_code",
                "title",
                "price_including_tax",
                "price_excluding_tax",
                "number_available",
                "product_description",
                "category",
                "review_rating",
                "image_url"
        )
        for column in columns:
            to_write += f"{column}{separator}"
        file.write(to_write[0:-1] + "\n")
        for book in books:
            to_write = ""
            for column in columns:
                to_write += f"{book[column]}{separator}"
            try:
                file.write(to_write[0:-1] + "\n")
            except UnicodeEncodeError:
                print(f"<!> Erreur de caractères : {book['title']} <!>")
                pass
        file.close()


def main():

    try:
        os.mkdir(results_dir_name)
    except FileExistsError:
        pass

    soup = get_soup("https://books.toscrape.com/")
    categories = get_categories(soup)
    books = {}
    """
    for category_name, category_url in categories.items():
        # print(f"{counter}. {category_name}: {category_url}")
        books[category_name] = get_books_infos_from_category(category_name, category_url)
        generate_csv(category_name, books[category_name])
    """
    books["Suspense"] = get_books_infos_from_category("Suspense", "https://books.toscrape.com/catalogue/category/books/suspense_44/")
    generate_csv("Suspense", books["Suspense"])


if __name__ == '__main__':
    main()