import requests
from bs4 import BeautifulSoup
import urllib.request
import csv
import os

url = "https://books.toscrape.com/"


def make_dir():
    os.system("mkdir Images")
    os.system("mkdir CSV_Files")


def url_to_jpg(image_url, file_path):
    filename = image_url.split("/")[8]
    full_path = "{}{}".format(file_path, filename)
    urllib.request.urlretrieve(image_url, full_path)
    # print('{} saved'.format(filename))
    return None


def get_book_info(book_url):
    """
    This function is used to get all info about a book from his url.
    This function only work with book.toscrape.com.

    Args:
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
    upc = ""
    title = ""
    pit = ""
    pet = ""
    na = ""
    pd = ""
    category = ""
    rr = ""
    image_url = ""
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
        image_url = url + soup.find("img").attrs["src"].replace("../../", "/")
    else:
        print("Status Code: " + str(page.status_code))
    return book_url, upc, title, pit, pet, na, pd, category, rr, image_url


def get_category(category_url):
    page = requests.get(category_url)
    soup = BeautifulSoup(page.content, "html.parser")
    links = []
    category_name = soup.findAll("div", class_="page-header")
    h3s = soup.findAll("h3")
    for h3 in h3s:
        links.append(
            url + h3.find("a").attrs["href"].replace("../../../", "catalogue/")
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
                url + h3.find("a").attrs["href"].replace("../../../", "catalogue/")
            )
    return category_name, links


def write_csv(cat_name, cat_data):
    header = [
        "Product URL",
        "Universal Product Code",
        "Title",
        "Price Including Tax",
        "Price Excluding Tax",
        "Number Available",
        "Product Description",
        "Category",
        "Review Rating",
        "Image  URL",
    ]
    csvfile = open("CSV_Files/" + cat_name, "w", newline="", encoding="utf8")
    c = csv.writer(csvfile)
    c.writerow(header)
    for i in range(len(cat_data)):
        c.writerow(cat_data[i])
        i += 1
    csvfile.close()
    return None


"""
def get_all():
    a = []
    cat = []
    header = [
        "Product URL",
        "Universal Product Code",
        "Title",
        "Price Including Tax",
        "Price Excluding Tax",
        "Number Available",
        "Product Description",
        "Category",
        "Review Rating",
        "Image  URL",
    ]
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    links = soup.find(class_="nav-list").find("ul").findAll("a")
    categories = soup.find(class_="nav-list").find("ul").findAll("a")
    for category in categories:
        cat.append(category.text.strip().replace(" ", "-") + ".csv")
    for link in links:
        a.append(url + link.attrs["href"])
    i = 0
    while i != len(a):
        csvfile = open("CSV_Files/" + cat[i], "w", newline="", encoding="utf8")
        c = csv.writer(csvfile)
        c.writerow(header)
        print("Getting category " + cat[i].replace(".csv", "") + " data !")
        get_category(a[i])
        for ii in range(len(book_urls)):
            row = [
                book_urls[ii],
                upcs[ii],
                titles[ii],
                pit[ii],
                pet[ii],
                na[ii],
                pd[ii],
                cate[ii],
                rr[ii],
                image_urls[ii],
            ]
            c.writerow(row)
        csvfile.close()
        i += 1
"""
