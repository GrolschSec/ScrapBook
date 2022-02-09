import requests
from bs4 import BeautifulSoup
import urllib.request
import csv
import os


def make_dir(dir_name):
    os.system("mkdir " + dir_name)
    return None


def url_to_jpg(image_url, file_path):
    filename = image_url.split("/")[8]
    full_path = "{}{}".format(file_path, filename)
    urllib.request.urlretrieve(image_url, full_path)
    return None


def get_book_info(base_url, book_url):
    """
    This function is used to get all info about a book from his url.
    This function only work with book.toscrape.com.

    Args:
        base_url: Main url of the website.
        book_url: The url of the book.

    Return:
        book_url: The url of the book.
        upc: The universal product code.
        title: The title of the book.
        pit: The price including tax.
        pet: The price excluding tax.
        pd: The product description.
        category: The category of book.
        rr: The rate review.
        image_url: The url of the image to descript the book.
    """
    page = requests.get(book_url)
    if page.ok:
        soup = BeautifulSoup(page.content, "html.parser")
        book_swap = soup.find_all("td", class_=False)
        upc = book_swap[0].text
        title = soup.find("h1").text
        pit = book_swap[3].text
        pet = book_swap[2].text
        na = book_swap[5].text.split(" ")[2].replace("(", "")
        pd = soup.find_all("p")[3].text
        category = soup.find_all("a")[3].text
        rr = soup.find("p", class_="star-rating").attrs["class"][1]
        image_url = base_url + soup.find("img").attrs["src"].replace("../../", "/")
        dico = {
            "product_url": book_url,
            "universal_product_code": upc,
            "title": title,
            "price_including_tax": pit,
            "price_excluding_tax": pet,
            "number_available": na,
            "product_description": pd,
            "category": category,
            "review_rating": rr,
            "image_url": image_url,
        }
        return dico, image_url
    else:
        print("Status Code: " + str(page.status_code))


def get_category(base_url, category_url):
    page = requests.get(category_url)
    soup = BeautifulSoup(page.content, "html.parser")
    links = []
    category_name = soup.find("div", class_="page-header").find("h1").text
    h3s = soup.findAll("h3")
    for h3 in h3s:
        links.append(
            base_url + h3.find("a").attrs["href"].replace("../../../", "catalogue/")
        )
    while soup.find(class_="next"):
        new_link = category_url.split("/")
        del new_link[7]
        new_link.append(soup.find(class_="next").find("a").attrs["href"])
        deli = "/"
        temp = list(map(str, new_link))
        new_link = deli.join(temp)
        page = requests.get(new_link)
        soup = BeautifulSoup(page.content, "html.parser")
        h3s = soup.findAll("h3")
        for h3 in h3s:
            links.append(
                base_url + h3.find("a").attrs["href"].replace("../../../", "catalogue/")
            )
    return category_name, links


def write_csv(csv_path, cat_name, dico):
    header = [
        "Product URL",
        "Universal Product Code",
        "Title",
        "Price including tax",
        "Price excluding tax",
        "Number available",
        "Product description",
        "Category",
        "Review rating",
        "Image URL",
    ]
    csvfile = open(csv_path + cat_name + ".csv", "w", newline="", encoding="utf8")
    c = csv.writer(csvfile)
    c.writerow(header)
    for data in dico:
        c.writerow(data.values())
    csvfile.close()
    return None
