ScrapBook is a Scraping tool made to scrap the content of the website: 
"book.toscrape.com"

While it is in action it get information by book:
 - Product URL
 - Universal Product Code
 - Title of the book
 - Price Including Tax
 - Price Excluding Tax 
 - Number Available
 - Product Description
 - Category 
 - Review Rating
 - Book Image URL

Then it class this datas in a CSV file by category.

Each CSV files are located in the directory 'CSV_Files'.

The Script also get the Book Image 'jpg' and add them to the directory 'Images'.



Instalation:

- Clone the github repository:
  - git clone https://github.com/GrolschSec/ScrapBook.git
- Go to ScrapBook directory:
  - cd ScrapBook
- Create a virtual environments using python3 venv tool:
  - python3 -m venv env
- Load the virtual environment:
  - source env/bin/activate
- Install the requirements for the script:
  - python3 -m pip install -r requirements.txt


Running the script: 

  To run the script you have almost nothing to do.
  - Run using python3:
    - python3 main.py
  - The script asks you if you want to scrape the website, say yes:
    - Do you want to scrape the website ? (Y/N) y
  - Then let the script run until it stop by itself.
  - Once it's done you can check the Images and CSV in their own dir.