import requests
from bs4 import BeautifulSoup

url = 'https://books.toscrape.com/'


def get_book_info(book_url):
    page = requests.get(book_url)
    soup = BeautifulSoup(page.content, "html.parser")
    book_swap = soup.find_all('td', class_=False)

    upc = book_swap[0].text
    title = soup.find("h1").text
    price_including_tax = book_swap[3].text
    price_excluding_tax = book_swap[2].text
    number_available = book_swap[5].text.split(" ")[2].replace('(', '')
    product_description = soup.find_all('p')[3].text
    category = soup.find_all('a')[3].text
    review_rating = soup.find('p', class_="star-rating").attrs['class'][1]
    image_url = url + soup.find('img').attrs['src'].replace('../../', '/')

    print("UPC: " + upc + "\nTitle: " + title + "\nPrice (With tax): " + price_including_tax + "\n")
    print("Price (Without tax): " + price_excluding_tax + "\nNumber available: " + number_available + "\n")
    print("Description: " + product_description + "\nCategory: " + category + "\nRating: " + review_rating)
    print(image_url)


def get_category(category_url):
    page = requests.get(category_url)
    soup = BeautifulSoup(page.content, "html.parser")

