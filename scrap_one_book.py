
import requests
from bs4 import BeautifulSoup
import csv
import os

def get_request(url):
    """Récupère le contenu d'une page web et le retourne"""
    response = requests.get(url)
    response.encoding = "utf-8"
    return response

def get_soup(url):
    """Récupère le contenu d'une page web et le retourne sous forme de BeautifulSoup"""
    response = get_request(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def get_title(soup):
    """Récupère le titre d'un livre et le retourne"""
    return soup.find("div", class_="col-sm-6 product_main").h1.text

def get_category(soup):
    """Récupère la catégorie d'un livre et la retourne"""
    return soup.find_all("a")[3].text

def get_product_description(soup):
    """Récupère la description d'un livre et la retourne"""
    product_description = soup.find(id="product_description")
    if product_description:
        return soup.find(id="product_description").next_sibling.next_sibling.text
    else:
        return "No product description available"

def get_product_page_url(soup):
    """Récupère l'URL d'une page produit et la retourne"""
    return soup.find("div", class_="col-sm-6 product_main").h1.text

def get_universal_product_code(soup):
    """Récupère le code UPC d'un livre et le retourne"""
    return soup.find("th", text="UPC").next_sibling.text

def get_price_including_tax(soup):
    """Récupère le prix TTC d'un livre et le retourne"""
    return soup.find("th", text="Price (incl. tax)").next_sibling.text.replace("£", "")

def get_price_excluding_tax(soup):
    """Récupère le prix HT d'un livre et le retourne"""
    return soup.find("th", text="Price (excl. tax)").next_sibling.text.replace("£", "")

def get_number_available(soup):
    """Récupère le nombre d'exemplaires disponibles d'un livre et le retourne"""
    return soup.find("th", text="Availability").next_sibling.next_sibling.text.replace("In stock (", "").replace(" available)", "")

def get_review_rating(soup):
    """Récupère la note d'un livre et la retourne"""
    return soup.find("p", class_="star-rating")["class"][1].replace("One", "1").replace("Two", "2").replace("Three", "3").replace("Four", "4").replace("Five", "5")

def get_image_url(soup):
    """Récupère l'URL de l'image d'un livre et la retourne"""
    return soup.find("div", class_="item active").img["src"].replace("../..", "http://books.toscrape.com")

def get_book_infos(url):
    """Récupère toutes les informations d'un livre et les retourne"""
    soup = get_soup(url)
    return {
        "product_page_url": url,
        "universal_product_code": get_universal_product_code(soup),
        "title": get_title(soup),
        "price_including_tax": get_price_including_tax(soup),
        "price_excluding_tax": get_price_excluding_tax(soup),
        "number_available": get_number_available(soup),
        "product_description": get_product_description(soup),
        "category": get_category(soup),
        "review_rating": get_review_rating(soup),
        "image_url": get_image_url(soup)
    }

def fieldnames():
    """Retourne la liste des champs du fichier CSV"""
    return [
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
    ]

def filename():
    """Retourne le nom du fichier CSV"""
    return "output/onebook.csv"

def write_csv_file(filename, fieldnames, books_infos):
    """Écrit les informations d'un livre dans un fichier CSV"""
    with open(filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for book_infos in books_infos:
            writer.writerow(book_infos)
            print("Book infos written in CSV file" + " " + filename)

def scrape_one_book_image(image_url):
    """Télécharge l'image d'un livre"""
    response = requests.get(image_url)
    with open("output/onebook.jpg", "wb") as file:
        file.write(response.content)
        print("Book image downloaded in output folder" + " " + "onebook.jpg")

def main():
    print(""" --- Scraping one book --- 
    Veilleez entrer l'URL d'un livre à scraper :
    exemple : http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html
    """)
    url = input()
    os.makedirs("output", exist_ok=True)
    write_csv_file(filename(), fieldnames(), [get_book_infos(url)])
    scrape_one_book_image(get_book_infos(url)["image_url"])

main()