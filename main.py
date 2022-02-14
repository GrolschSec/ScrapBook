from utils import *

print("Welcome to ScrapBook !\nA Scrapping tool for book.toscrape.com\n")
user_input = user_input_attribution()
if user_input >= 1 and not user_input > 50:
    url = "https://books.toscrape.com/"
    make_dir("Images")
    make_dir("CSV_Files")
    categories = get_categories(url)
    i = 0
    while i != user_input:
        category = get_category(url, categories[i])
        category_name = category[0]
        links = category[1]
        data = []
        print("Getting info about books in category " + category_name)
        make_dir("Images/" + category_name)
        for link in links:
            x = get_book_info(url, link)
            data.append(x[0])
            url_to_jpg(x[1], "Images/" + category_name + "/")
        write_csv("CSV_Files/", category_name, data)
        i += 1
else:
    print("The input is wrong !!")
