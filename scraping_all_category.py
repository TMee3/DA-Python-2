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
def create_output_folder():
    """Crée le dossier output"""
    if not os.path.exists("output"):
        os.makedirs("output")

def create_category_folder(categories):
    """Crée un dossier pour une catégorie"""
    if not os.path.exists("output/" + categories):
        os.makedirs("output/" + categories)

def create_img_folder(categories):
    """Crée un dossier pour une catégorie"""
    if not os.path.exists("output/" + categories + "/img"):
        os.makedirs("output/" + categories + "/img")

def get_urls_from_category_page(url):
    """Récupère les URLs des livres d'une catégorie et les retourne"""
    soup = get_soup(url)
    urls = []
    next = soup.find("li", class_="next")
    for article in soup.find_all("article", class_="product_pod"):
        urls.append("http://books.toscrape.com/catalogue/" + article.h3.a["href"].replace("../", "").replace("index.html", ""))
    if next:
        urls += get_urls_from_category_page( url + next.a["href"])
    return urls


def scrape_category(url):
    """Récupère les informations de tous les livres d'une catégorie et les écrit dans un fichier CSV"""
    urls = get_urls_from_category_page(url)
    books_infos = []
    for url in urls:
        books_infos.append(get_book_infos(url))
    return books_infos

def main_url():
    """Retourne l'URL de la page d'accueil du site"""
    return "http://books.toscrape.com/index.html"

def get_categories_urls():
    """Récupère les URLs des catégories et les retourne"""
    soup = get_soup(main_url())
    urls = []
    for li in soup.find("ul", class_="nav nav-list").find("ul").find_all("li"):
        urls.append("http://books.toscrape.com/" + li.a["href"].replace("../", "").replace("index.html", ""))
    return urls

def get_categories():
    """Récupère les catégories et les retourne"""
    soup = get_soup(main_url())
    categories = []
    for li in soup.find("ul", class_="nav nav-list").find("ul").find_all("li"):
        categories.append(li.a.text.strip())
    return categories


def write_csv_file(filename, fieldnames, books_infos):
    """Ecrit les informations des livres dans un fichier CSV"""
    with open(filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for book in books_infos:
            writer.writerow(book)
            print("Book added to CSV file : " + book["title"] + " " + filename)

def filename(categories):
    """Retourne le nom du fichier CSV"""
    return "output/" + categories + "/" + categories + ".csv"

def scrape_img(url, categories, title):
    """Récupère les images des livres et les écrit dans un fichier"""
    response = requests.get(url)
    with open("output/" + categories + "/img/" + title + ".jpg", "wb") as file:
        file.write(response.content)
        print("Image " + title + " téléchargée" + " dans le dossier " + categories)
    


def scrape_all():
    """Récupère les informations de tous les livres de toutes les catégories et les écrit dans un fichier CSV"""
    for category in get_categories():
        create_output_folder()
        create_category_folder(category)
        print("Dossier créé pour la catégorie " + category)
        create_img_folder(category)
        print("Dossier créé pour les images de la catégorie " + category)
        print("Scraping " + category + " category...")
        books_infos = scrape_category(get_categories_urls()[get_categories().index(category)])
        write_csv_file(filename(category), fieldnames(), books_infos)
        print("Scraping " + category + " category done.")
        for book in books_infos:
            scrape_img(book["image_url"], category, book["title"].replace("/", "-"))


def main():
    """Fonction principale"""
    scrape_all()

main()