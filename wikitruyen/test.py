from lxml import html

# Nội dung HTML cần xử lý
html_content = '''
<div class="truyen">
    Triệu Tử Tu ổn định trong tay dù, nói tiếp nói: “Có thể là lần trước ngồi chính là du thuyền, lần này ngồi chính là thương thuyền đi. Bất quá ta nhưng thật ra cảm thấy đều không sai biệt lắm.”<br><br>
    “Phải không?” Từ Nhược Ảnh cười tủng tủng, lại nói: “Ngươi nói, đại ca cùng tẩu tẩu như thế nào như vậy ngồi được? Này rất tốt phong cảnh không ra xem, cư nhiên ở trong phòng chơi cờ. Hảo nhàm chán a ～”<br><br>
    “Bọn họ hai cái tính cách trầm ổn, ngồi được cũng rất bình thường.” Triệu Tử Tu nâng lên khác chỉ tay đáp ở nàng trên vai: “Cho nên bọn họ hai cái mới là phu thê sao.”<br><br>
    “Giống chúng ta hai cái, đều là ngồi không được, hợp nhau, cho nên cũng là phu thê.” Nói, Triệu Tử Tu cười một cái, hướng Từ Nhược Ảnh bên kia để sát vào chút.<br><br>
    Từ Nhược Ảnh lại ở trên mặt sông thấy cái thứ gì, đột nhiên kinh hỉ lên, bắt lấy bên người Triệu Tử Tu quần áo: “Tử tu mau xem, bên kia thật lớn một con cá! Mau xem mau xem!”<br><br>
    Triệu Tử Tu: “……”<br><br>
    Hắn nhấp môi dưới, có điểm bất đắc dĩ. Cá có cái gì đẹp? Lại đại kia cũng là một con cá a.<br><br>
    Hắn hỏi: “Ta ở bên cạnh ngươi đứng, ngươi không xem ta, ngươi xem cá?”<br><br>
    Từ Nhược Ảnh như cũ nhìn giang mặt, tầm mắt một chút không dịch trở về, lại vẫn cho hắn giải thích nói: “Tử tu, ta mỗi ngày đều có thể thấy ngươi, nhưng như vậy đại một con cá, cũng không phải là tùy tùy tiện tiện là có thể thấy.”<br><br>
    Triệu Tử Tu tức khắc nghẹn lời.<br><br>
    Lời tuy như thế đi…… Nhưng, tổng cảm thấy nơi nào quái quái.<br><br>
    Không đúng, hắn vì sao phải cùng một con cá so? Hắn là cá nhân a!<br><br>
    Triệu Tử Tu kêu lên một tiếng, đem dù hoạt động vị trí đến chính mình trên đầu: “Ta không cao hứng, không cho ngươi bung dù.”<br><br>
    Từ Nhược Ảnh sửng sốt, cười quay đầu nhìn qua: “Đừng keo kiệt như vậy sao, ta chỉ là nhìn xem cá mà thôi.”<br><br>
    Triệu Tử Tu mị hạ mắt.<br><br>
    Từ Nhược Ảnh lập tức sửa miệng: “Hảo hảo, ta không xem cá, ta xem ngươi.”<br><br>
    Nàng cười nắm Triệu Tử Tu tay, làm nũng dường như quơ quơ: “Ta mỗi ngày đều xem ngươi!”<br><br>
</div>
'''

# Parse the HTML content
tree = html.fromstring(html_content)

# Lấy tất cả các đoạn văn
paragraphs = tree.xpath('//div[@class="truyen"]/text()')

# Chuyển các đoạn văn thành thẻ <p>
content = ''.join([f'<p>{p.strip()}</p>' for p in paragraphs if p.strip()])

print(content)