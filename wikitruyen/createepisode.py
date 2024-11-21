import json

# Đường dẫn tới tệp linkbook.json
input_file = 'linkbook.json'
# Đường dẫn tới tệp đầu ra
output_file = 'episodes.json'

def create_episodes(input_file, output_file):
    try:
        # Đọc dữ liệu từ file linkbook.json
        with open(input_file, 'r', encoding='utf-8') as f:
            books = json.load(f)
        
        episodes = []
        episode_id = 1  # ID tự tăng bắt đầu từ 1

        for book in books:
            book_id = book['id']
            slug = f"t{episode_id}-web-novel"
            episode_path = f"episode_path/{slug}.jpg"
            episode = {
                "id": str(episode_id),
                "book_id": str(book_id),
                "slug": slug,
                "episode_path": episode_path,
                "title": "Web Novel",
                "user_id": 1,
                "order": 1
            }
            episodes.append(episode)
            episode_id += 1

        # Ghi dữ liệu ra file episodes.json
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(episodes, f, ensure_ascii=False, indent=4)
        
        print(f"Đã tạo thành công file {output_file} với {len(episodes)} tập truyện.")
    
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy tệp {input_file}.")
    except json.JSONDecodeError:
        print(f"Lỗi: Tệp {input_file} không hợp lệ.")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

if __name__ == "__main__":
    create_episodes(input_file, output_file)
