from utils import *

url = "https://books.toscrape.com/"
make_dir('CSV_Files')
make_dir('Images')

category = get_category(url, 'http://books.toscrape.local/catalogue/category/books/fiction_10/index.html')
category_name = category[0]
links = category[1]
data = []
for link in links:
    x = get_book_info(url, link)
    data.append(x[0])
    url_to_jpg(x[1], 'Images/')
write_csv('CSV_Files/', category_name, data)
