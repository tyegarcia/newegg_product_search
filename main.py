from bs4 import BeautifulSoup
import requests
import re

# Search for any product on Newegg.com
# Sorts product in stock and by price

product = input("What product would you like to search for? ")

url = f"https://www.newegg.com/p/pl?d={product}&N=8000%204131"
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

# find number of pages for product
page_text = doc.find(class_="list-tool-pagination-text").strong
pages = int(str(page_text).split("/")[-2].split(">")[-1][:-1])

items_found = {}

# loops through each page in product
for page in range(1, pages + 1):
    url = f"https://www.newegg.com/p/pl?d={product}&N=8000%204131&page={page}"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")

    # this div contains actual product instead of searching in search bar
    div = doc.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")

    # re.compile finds any text that contains product
    items = div.find_all(text=re.compile(product))
    for item in items:
        parent = item.parent
        if parent.name != "a":
            continue

        link = parent['href']
        next_parent = item.find_parent(class_="item-container")
        try:
            price = next_parent.find(class_="price-current").find("strong").string
            items_found[item] = {"price": int(price.replace(",", "")), "link": link}
        except:
            pass

# creates tuple of sorted items by price
sorted_items = sorted(items_found.items(), key=lambda x: x[1]['price'])

# prints product, price, and link on new lines
for item in sorted_items:
    print(item[0])
    print(f"${item[1]['price']}")
    print(item[1]['link'])
    print("--------------------------------------------------------------")
