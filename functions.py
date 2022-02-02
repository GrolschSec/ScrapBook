import requests
from bs4 import BeautifulSoup

url_base = 'https://books.toscrape.com/'


def get_book_info(book_url):
    page = requests.get(book_url)
    if page.ok:
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
        image_url = url_base + soup.find('img').attrs['src'].replace('../../', '/')

        print("UPC: " + upc + "\nTitle: " + title + "\nPrice (With tax): " + price_including_tax + "\n")
        print("Price (Without tax): " + price_excluding_tax + "\nNumber available: " + number_available + "\n")
        print("Description: " + product_description + "\nCategory: " + category + "\nRating: " + review_rating)
        print(image_url)
    else:
        print("Status Code: " + str(page.status_code))


def get_category(category_url):
    page = requests.get(category_url)
    if page.ok:
        soup = BeautifulSoup(page.content, "html.parser")
        links = []
        h3s = soup.findAll("h3")
        for h3 in h3s:
            a = url_base + h3.find('a').attrs['href'].replace('../../../', 'catalogue/')
            links.append(a)
        for link in links:
            get_book_info(link)
        
        if int(soup.findAll("strong")[1].text) > 20:
            if int(soup.find(class_="current").text.split()[1]) < int(soup.find(class_="current").text.split()[3]):
                new_link = category_url.split('/')
                del new_link[7]
                new_link.append(soup.find(class_="next").find('a').attrs['href'])
                deli = '/'
                temp = list(map(str, new_link))
                res = deli.join(temp)
                print(res)
                get_category(res)
    else:
        print("Status Code: " + str(page.status_code))


def get_all(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    a = []
    links = soup.find(class_="nav-list").find("ul").findAll('a')
    for link in links:
        a.append(url_base + link.attrs['href'])
    i = 0
    while i != (len(a) - 1):
        get_category(a[i])
        i += 1
