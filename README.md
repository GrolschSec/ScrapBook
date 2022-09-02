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

Then it classes this datas in a CSV file by category.

Each CSV files are located in the directory 'CSV_Files'.

The Script also get the Book Image 'jpg' and add them to the directory 'Images'.



Installation:

- Clone the GitHub repository:
```
git clone https://github.com/GrolschSec/ScrapBook.git
```
- Go to ScrapBook directory:
```
cd ScrapBook
```
- Create a virtual environments using python3 venv tool:
```
python3 -m venv env
```
- Load the virtual environment:
```
source env/bin/activate
```
- Install the requirements for the script:
```
python3 -m pip install -r requirements.txt
```


Running the script: 

  To run the script you have almost nothing to do.
  - Run using python3:
    - python3 main.py
    - The script ask you if you want to get all categories or a number of categories:
      - If you type 1 then it downloads all categories automatically.
      - If you type 2 it asks you how many categories you want to scrape on the website: 
        - Enter a number between 1 and 50.
  - Then let the script run until it stop by itself.
  - Once it's done you can check the Images and CSV in their own dir.
