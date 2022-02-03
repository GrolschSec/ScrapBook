import requests
from bs4 import BeautifulSoup
import urllib.request
import csv
import os

url = 'https://books.toscrape.com/'
book_urls = []
upcs = []
titles = []
pit = []
pet = []
na = []
pd = []
cate = []
rr = []
image_urls = []


def make_dir():
    os.system("mkdir Images")
    os.system("mkdir CSV_Files")


def clear_global():
    book_urls.clear()
    upcs.clear()
    titles.clear()
    pit.clear()
    pet.clear()
    na.clear()
    pd.clear()
    cate.clear()
    rr.clear()

def url_to_jpg(image_url, file_path):
    filename = image_url.split('/')[8]
    full_path = '{}{}'.format(file_path, filename)
    urllib.request.urlretrieve(image_url, full_path)
    # print('{} saved'.format(filename))
    return None


def get_book_info(book_url):
    page = requests.get(book_url)
    if page.ok:
        soup = BeautifulSoup(page.content, "html.parser")
        book_swap = soup.find_all('td', class_=False)
        book_urls.append(book_url)
        upcs.append(book_swap[0].text)
        titles.append(soup.find("h1").text)
        pit.append(book_swap[3].text)
        pet.append(book_swap[2].text)
        na.append(book_swap[5].text.split(" ")[2].replace('(', ''))
        pd.append(soup.find_all('p')[3].text)
        cate.append(soup.find_all('a')[3].text)
        rr.append(soup.find('p', class_="star-rating").attrs['class'][1])
        image_url = url + soup.find('img').attrs['src'].replace('../../', '/')
        image_urls.append(image_url)
        url_to_jpg(image_url, "Images/")
    else:
        print("Status Code: " + str(page.status_code))


def get_category(category_url):
    page = requests.get(category_url)
    if page.ok:
        soup = BeautifulSoup(page.content, "html.parser")
        links = []
        h3s = soup.findAll("h3")
        for h3 in h3s:
            a = url + h3.find('a').attrs['href'].replace('../../../', 'catalogue/')
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
                get_category(res)
    else:
        print("Status Code: " + str(page.status_code))


def get_all():
    a = []
    cat = []
    header = [
        'Product URL',
        'Universal Product Code',
        'Title',
        'Price Including Tax',
        'Price Excluding Tax',
        'Number Available',
        'Product Description',
        'Category',
        'Review Rating',
        'Image URL'
               ]
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    links = soup.find(class_="nav-list").find("ul").findAll('a')
    categories = soup.find(class_="nav-list").find("ul").findAll('a')
    for category in categories:
        cat.append(category.text.strip().replace(' ', '-') + '.csv')
    for link in links:
        a.append(url + link.attrs['href'])
    i = 0
    while i != len(a):
        csvfile = open('CSV_Files/' + cat[i], 'w', newline='', encoding='utf8')
        c = csv.writer(csvfile)
        c.writerow(header)
        print("Getting category " + cat[i].replace('.csv', '') + " data !")
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
                image_urls[ii]
            ]
            c.writerow(row)
        clear_global()
        csvfile.close()
        i += 1
