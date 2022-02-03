from functions import *

print("ScrapBook: A Scrapper for 'books.toscrape.com'")
user_input = input("Do you want to scrape the website ? (Y/N) ")

if user_input == "Y" or user_input == "y":
    print("Scraping the whole website...")
    make_dir()
    get_all()
elif user_input == "N" or user_input == "n":
    print("Come back later")
else:
    print("Unknown option !")
