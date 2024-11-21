import requests
from bs4 import BeautifulSoup
import json
import os

# The URL of the page to scrape
url = 'https://metruyenchu.com.vn/danh-sach/truyen-full?page=1'  # Replace with the actual URL

# Send a GET request to the URL
response = requests.get(url)

# List to store the scraped data
books = []

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the 'item' divs inside 'truyen-list'
    items = soup.find_all('div', class_='item')

    # Loop through each item and extract the title and URL
    for item in items:
        # Find the 'a' tag with class 'cover' or 'h3' for the title
        link_tag = item.find('a', title=True)  # Finds the 'a' with the title attribute
        if link_tag:
            title = link_tag.get('title')
            url = link_tag.get('href')

            # Append the title, URL, and ID to the books list
            books.append({
                'title': title,
                'url': url
            })

    # Check if the file 'linkbook.json' exists
    if os.path.exists('linkbook.json'):
        # If the file exists, read the current content and append the new data
        with open('linkbook.json', 'r', encoding='utf-8') as f:
            existing_books = json.load(f)

        # Set the starting ID based on the last ID in the existing file
        start_id = existing_books[-1]['id'] + 1 if existing_books else 1

        # Add ID to each new book and append to existing books
        for i, book in enumerate(books):
            book['id'] = start_id + i  # Assign ID to each book

        existing_books.extend(books)  # Add the new books to the existing list

        # Write the updated list back to the file
        with open('linkbook.json', 'w', encoding='utf-8') as f:
            json.dump(existing_books, f, ensure_ascii=False, indent=4)

    else:
        # If the file doesn't exist, create a new one and write the books with IDs
        for i, book in enumerate(books):
            book['id'] = i + 1  # Assign ID starting from 1

        with open('linkbook.json', 'w', encoding='utf-8') as f:
            json.dump(books, f, ensure_ascii=False, indent=4)

    print(f'Scraped {len(books)} books and saved to linkbook.json')

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
