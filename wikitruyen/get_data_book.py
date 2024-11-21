import json
import os
import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
import re

# Base URL
base_url = "https://metruyenchu.com.vn"

# Đọc file linkbook.json
with open('linkbook.json', 'r', encoding='utf-8') as file:
    linkbook_data = json.load(file)

# Kết quả
results = []

# Hàm làm sạch tên file
def clean_filename(filename):
    # Thay thế các ký tự không hợp lệ bằng dấu gạch ngang hoặc loại bỏ chúng
    return re.sub(r'[<>:"/\\|?*]', '-', filename)

for book in linkbook_data:
    full_url = base_url + book['url']
    response = requests.get(full_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Lấy ảnh bìa
        img_tag = soup.select_one('.book-info-pic img')
        image_url = base_url + img_tag['src'] if img_tag else None

        # Lấy tác giả
        author_tag = soup.select_one('li:has(b:-soup-contains("Tác giả:")) a')
        author = author_tag.text.strip() if author_tag else "không có"

        # Lấy mô tả từ XPath mới
        description_tag = soup.select_one('#gioithieu > div:nth-of-type(1) > div')
        description = description_tag.get_text(separator="\n").strip() if description_tag else "Không có mô tả"

        # Tạo slug
        slug = f"{book['id']}-{unidecode(book['title']).lower().replace(' ', '-')}"

        # Làm sạch slug trước khi tạo tên file
        clean_slug = clean_filename(slug)

        # Tạo các trường khác
        result = {
            "id": book['id'],
            "title": book['title'],
            "image_url": image_url,
            "slug": clean_slug,
            "author": author,
            "description": description,
            "view": int(round(1000 + 90000 * (book['id'] % 7) / 7)),  # Random view, đổi thành số nguyên
            "like": book['id'] * 10 + 100,
            "note": "Tạo bài viết",
            "status": 3  # Mặc định status là 3
        }

        # Tải ảnh về thư mục `book_path`
        if image_url:
            image_name = f"book_path/{clean_slug}.jpg"
            os.makedirs('book_path', exist_ok=True)
            img_data = requests.get(image_url).content
            with open(image_name, 'wb') as img_file:
                img_file.write(img_data)
            result['image_url'] = image_name  # Cập nhật đường dẫn ảnh cục bộ

        results.append(result)
    else:
        print(f"Failed to fetch {full_url}")

# Ghi kết quả vào file book_data.json
with open('book_data.json', 'w', encoding='utf-8') as file:
    json.dump(results, file, ensure_ascii=False, indent=4)

print("Dữ liệu đã được ghi vào file book_data.json")
