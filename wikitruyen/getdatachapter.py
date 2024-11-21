import json
import requests
from lxml import html
import re
from unidecode import unidecode

# Biến toàn cục để lưu ID chương
global_chapter_id = 1

# Đọc dữ liệu từ file JSON
def read_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File {file_path} không tồn tại.")
    except json.JSONDecodeError:
        print(f"Lỗi: Không thể giải mã JSON từ file {file_path}.")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")
    return None

# Lưu dữ liệu vào file JSON
def append_to_json(data, file_path):
    try:
        with open(file_path, 'r+', encoding='utf-8') as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = []
            file.seek(0)
            file.truncate()
            existing_data.append(data)
            json.dump(existing_data, file, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump([data], file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Lỗi khi ghi vào file JSON: {e}")

# Chuyển đổi tiêu đề thành slug
def convert_to_slug(title):
    title = unidecode(title.strip())
    title = title.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', title)
    slug = re.sub(r'[\s-]+', '-', slug)
    return slug

# Lấy URL chương đầu tiên từ trang sách
def get_start_url(book_url, base_url, headers):
    try:
        print(f"Đang truy cập trang sách: {book_url}")
        response = requests.get(book_url, headers=headers)
        response.raise_for_status()

        tree = html.fromstring(response.content)
        start_url_relative = tree.xpath('//*[@id="chapter-list"]/div[1]/ul[1]/li[1]/a/@href')
        
        if not start_url_relative:
            print(f"Không tìm thấy chương đầu tiên tại {book_url}.")
            return None
        
        start_url = base_url + start_url_relative[0]
        print(f"URL chương đầu tiên: {start_url}")
        return start_url
    except requests.RequestException as e:
        print(f"Lỗi khi truy cập {book_url}: {e}")
    except Exception as e:
        print(f"Lỗi không xác định khi lấy chương đầu tiên: {e}")
    return None

# Lấy thông tin từ một chương và điều hướng qua nút "Next"
def get_chapters_by_navigation(start_url, book_id, headers):
    global global_chapter_id
    all_chapters_info = []
    current_url = start_url

    while current_url:
        try:
            print(f"Đang truy cập chương: {current_url}")
            response = requests.get(current_url, headers=headers)
            response.raise_for_status()

            tree = html.fromstring(response.content)
            chapter_title = tree.xpath('//*[@id="vungdoc"]/div[1]/div[1]/h2/a/text()')
            chapter_content = tree.xpath('//*[@id="vungdoc"]/div[2]//text()')
            next_chapter_url = tree.xpath('//*[@id="gotochap"]/a[3]/@href')

            if not chapter_title:
                print(f"Không tìm thấy tiêu đề tại {current_url}")
                break

            title = chapter_title[0].strip()
            content_paragraphs = [f"<p>{c.strip()}</p>" for c in chapter_content if c.strip()]
            content = "".join(content_paragraphs)
            word_count = sum(len(c.split()) for c in chapter_content if c.strip())
            chapter_slug = f"c{global_chapter_id}-{convert_to_slug(title)}"

            chapter_info = {
                "title": title,
                "url": current_url,
                "slug": chapter_slug,
                "book_id": str(book_id),
                "episode_id": str(book_id),
                "id": global_chapter_id,  # Sử dụng ID toàn cục
                "content": content,
                "word_count": word_count
            }
            all_chapters_info.append(chapter_info)

            # Chuyển đến chương tiếp theo
            if next_chapter_url:
                current_url = next_chapter_url[0]
                if not current_url.startswith("http"):
                    current_url = f"https://metruyenchu.com.vn{current_url}"
            else:
                print("Không tìm thấy chương tiếp theo.")
                break

            global_chapter_id += 1  # Tăng ID toàn cục

        except requests.RequestException as e:
            print(f"Lỗi khi truy cập {current_url}: {e}")
            break
        except Exception as e:
            print(f"Lỗi không xác định tại {current_url}: {e}")
            break

    return all_chapters_info

# Xử lý toàn bộ sách trong linkbook.json
def process_books(file_path, output_path, base_url):
    linkbook_data = read_json(file_path)
    if not linkbook_data:
        print(f"Không có dữ liệu sách để xử lý từ {file_path}.")
        return

    headers = {'User-Agent': 'Mozilla/5.0'}
    for book in linkbook_data:
        book_url = base_url + book['url']
        start_url = get_start_url(book_url, base_url, headers)
        
        if start_url:
            chapters_info = get_chapters_by_navigation(start_url, book['id'], headers)
            for chapter in chapters_info:
                append_to_json(chapter, output_path)

# Chạy chương trình
if __name__ == "__main__":
    base_url = "https://metruyenchu.com.vn"
    input_file = "linkbook.json"
    output_file = "data_chapter.json"
    process_books(input_file, output_file, base_url)
