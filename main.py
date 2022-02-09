from utils import *

print("Welcome to ScrapBook !\nA Scrapping tool for book.toscrape.com\n")
make_dir("Images")
make_dir("CSV_Files")
url = "https://books.toscrape.com/"
user_input = int(input("Choose a number of category to scrape (min: 1, max: 50): "))
if user_input >= 1:
    categories = get_categories(url)
    i = 0
    while i != user_input:
        category = get_category(url, categories[i])
        category_name = category[0]
        links = category[1]
        data = []
        print('Getting info about books in category ' + category_name)
        for link in links:
            x = get_book_info(url, link)
            data.append(x[0])
            url_to_jpg(x[1], "Images/")
        write_csv("CSV_Files/", category_name, data)
        i += 1
elif user_input is str or user_input > 1 or user_input > 51:
    print("The input is wrong !!")
