import requests
from bs4 import BeautifulSoup
import urllib.request
import csv
import os


def make_dir(dir_name):
    """
    make_dir is a simple function that make a directory in the working directory

    Args:
        dir_name: The name you want for your directory.
    """
    os.system("mkdir " + dir_name)
    return None


def url_to_jpg(image_url, file_path):
    """
    url_to_jpg is a function that download jpg image from an url and save it to a directory.

    Args:
        image_url: The URL of the image you want to download.
        file_path: The directory you designed to save the image.
    """
    filename = image_url.split("/")[8]
    full_path = "{}{}".format(file_path, filename)
    urllib.request.urlretrieve(image_url, full_path)
    return None


def get_book_info(base_url, book_url):
    """
    This function is used to get all info about a book from his url.

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
    """
    This function is used to get the links of all books of a category.

    Args:
        base_url: The main url of the website (just to make the new link for other pages).
        category_url: The url of the category.

    Returns:
        category_name: The name of the category.
        links: The list of the links from all books of the category.
    """
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


def get_categories(url):
    """
    A function to get the links of all categories.

    Args:
        url: The main url of the website.

    Returns:
        A list of all the links of the categories.
    """
    categories = []
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    links = soup.find(class_="nav-list").find("ul").findAll("a")
    for link in links:
        categories.append(url + link.attrs["href"])
    return categories


def write_csv(csv_path, cat_name, dico):
    """
    A function to write data in a CSV file.

    Args:
        csv_path: The path to save the csv files.
        cat_name: The category name that we will use to name the csv file.
        dico: The dictionary with the data that we want to write in the csv file.
    """
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
