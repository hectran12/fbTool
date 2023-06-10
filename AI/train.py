import requests
import sys
import random
sys.path.append('./')
from loader import conf

config = conf.config
url = config.get('api_ai', 'urlAPI')

def ask (question: str) -> requests.post:
    return requests.post(
        url,
        data = {
            'ask': question
        }
    )

def randomMessageVietnamese () -> str:
    character = '''Xin chào
Tạm biệt
Cảm ơn
Xin lỗi
Xin vui lòng
Đúng
Sai
Tốt
Xấu
Đẹp
Giàu
Nghèo
Thành công
Thất bại
Hạnh phúc
Buồn
Vui
Yêu
Ghét
Công việc
Gia đình
Bạn bè
Trường học
Bác sĩ
Kỹ sư
Giáo viên
Nông dân
Sinh viên
Thể thao
Âm nhạc
Nghệ thuật
Đọc sách
Xem phim
Du lịch
Mua sắm
Ẩm thực
Hẹn hò
Thời gian
Tiền bạc
Giao thông
Đường phố
Nhà hàng
Quán café
Rạp chiếu phim
Cửa hàng
Bưu điện
Bệnh viện
Nhà thờ
Chùa
Cầu
Sông
Biển
Núi
Cánh đồng
Vườn
Hoa
Cây
Thú cưng
Máy tính
Điện thoại
Internet
Xe hơi
Xe máy
Xe đạp
Máy bay
Tàu hỏa
Ga tàu
Bến xe
Trạm xăng
Ngân hàng
Siêu thị
Chợ
Trung tâm thương mại
Công viên
Bể bơi
Sân vận động
Nhà hàng nhanh
Nhà hàng Buffet
Nhà hàng Việt
Quán phở
Quán cơm
Bún chả
Bánh mì
Bánh xèo
Chè
Trà sữa
Bia
Rượu
Nước ngọt
Trái cây
Thịt
Hải sản
Rau củ
Mỳ gói
Thịt bò
Thịt lợn
Thịt gà
Cá
Mực
Bánh tráng.'''
    keywords = character.split('\n')
    keywords = [i for i in keywords if i != '']
    result = ''
    for char in range(5):
        result += random.choice(keywords) + ' '
    return result
def getSuggetTopic () -> str:
    topics = '''Biến đổi khí hậu
Công nghệ trí tuệ nhân tạo (AI)
Blockchain và tiền điện tử
Mạng 5G
Internet of Things (IoT)
Tự lái ô tô
Vũ trụ và khám phá không gian
Giảm thiểu rác thải nhựa
Phát triển năng lượng tái tạo
Máy bay không người lái (drone)
Bảo vệ dữ liệu và quyền riêng tư trực tuyến
Chống khủng bố và an ninh toàn cầu
Xã hội mạng và truyền thông xã hội
Tái cơ cấu kinh tế toàn cầu
Cuộc cách mạng công nghiệp 4.0
Kỹ thuật sản xuất điện gió và năng lượng mặt trời
Phát triển bền vững và xanh
Sức khỏe tâm thần và trầm cảm
Truyền thông và thông tin giả mạo
Hệ thống chính trị và bầu cử
Cuộc sống số và tương tác trực tuyến
Bảo tồn động vật hoang dã và đa dạng sinh học
Cải cách giáo dục và đào tạo
Cải cách y tế và phòng ngừa bệnh
Công bằng và quyền dân sự
Kỹ thuật in 3D
Cuộc cách mạng công nghiệp hóa nông nghiệp
Nghệ thuật và văn hóa đương đại
Chuyển đổi số và sự tự động hóa
Cuộc sống du lịch và du lịch bền vững
Tăng trưởng kinh tế và phát triển kinh tế
Cải cách tài chính và ngân hàng
Trí tuệ nhân tạo trong dịch vụ khách hàng
Chiến tranh thương mại và thỏa thuận thương mại
Bạo lực và tội phạm trực tuyến
Giáo dục đại chúng và truyền thông đại chúng
Tăng cường an ninh mạng và phòng chống tấn công mạng
Cải cách luật pháp và hệ thống tư pháp
Quản lý tài chính cá nhân và đầu tư
Phụ nữ và quyền lợi giới tính
Tổ chức phi chính phủ và hoạt động phi lợi nhuận
Cải cách hệ thống chăm sóc sức khỏe
Phòng ngừa dịch bệnh và kiểm soát dịch tễ
Sản xuất và sử dụng ô tô điện
Phát triển công nghệ sinh học và y tế
Sự phân hóa kinh tế và thu nhập
Thay đổi trong ngành công nghiệp phim và truyền hình
Cải cách tài trợ giáo dục và học phí đại học
Đổi mới và sáng tạo trong doanh nghiệp
Phòng chống nạn buôn người và lao động trái phép
Sự phát triển của eSports và ngành công nghiệp trò chơi điện tử
Kỹ thuật máy tính và trí tuệ nhân tạo trong y tế
Quản lý tài nguyên nước và bảo vệ môi trường
Sự tăng trưởng của thương mại điện tử và mua sắm trực tuyến
Cải cách hệ thống chính trị và cơ quan quản lý
Cách mạng xanh và phát triển bền vững
Quyền lực và ảnh hưởng của các công ty công nghệ lớn
Kỹ thuật số hóa và quản lý thông tin
Thực phẩm và nhu cầu dinh dưỡng toàn cầu
Sự thay đổi của ngành công nghiệp âm nhạc
Tăng cường an ninh và phòng ngừa khủng bố
Cải cách hệ thống giáo dục phổ thông
Phát triển trí tuệ nhân tạo trong ngành nông nghiệp
Hòa giải và giải quyết xung đột
Tăng cường đào tạo và phát triển nhân lực
Nghiên cứu về bệnh tật và tìm kiếm biện pháp chữa trị
Sáng tạo xã hội và giải quyết vấn đề xã hội
Tăng cường quản lý rủi ro và an toàn
Hòa bình và đối thoại quốc tế
Cải cách hệ thống tiền tệ toàn cầu
Phát triển năng lượng hạt nhân và sử dụng an toàn
Cải cách hệ thống bảo vệ xã hội
Phát triển công nghệ và ứng dụng trí tuệ nhân tạo trong công nghiệp
Sáng tạo kỹ thuật và tương lai của ngành xây dựng
Tăng cường công bằng giới và đa dạng
Cải cách hệ thống thuế và phí
Phát triển công nghệ và ứng dụng trí tuệ nhân tạo trong ngành dầu khí
Đổi mới trong ngành công nghiệp thực phẩm và đồ uống
Tăng cường hợp tác quốc tế và đối tác đa phương
Cải cách hệ thống chăm sóc trẻ em và người già
Công nghệ giáo dục và học trực tuyến
Phát triển và sử dụng năng lượng thủy điện
Tăng cường an ninh hàng không và sự an toàn
Cải cách hệ thống định cư và di dân
Phát triển công nghệ và ứng dụng trí tuệ nhân tạo trong ngành y tế
Sáng kiến và kỹ thuật xã hội
Tăng cường quản lý và phòng ngừa thảm họa tự nhiên
Cải cách hệ thống pháp luật và tư pháp
Phát triển công nghệ và ứng dụng trí tuệ nhân tạo trong ngành sản xuất
Đổi mới trong ngành công nghiệp thể thao và giải trí
Tăng cường quản lý và bảo vệ đất đai
Cải cách hệ thống chăm sóc sức khỏe tâm thần
Sáng tạo và công nghệ trong ngành nghệ thuật và giải trí
Tăng cường quản lý rừng và bảo vệ môi trường rừng
Cải cách hệ thống vận tải công cộng và giao thông
Phát triển công nghệ và ứng dụng trí tuệ nhân tạo trong ngành bán lẻ
Hợp tác quốc tế trong nghiên cứu khoa học và phát triển công nghệ
Tăng cường quản lý và bảo vệ đại dương và nguồn tài nguyên biển
Cải cách hệ thống chăm sóc sức khỏe sinh sản và gia đình
Phát triển công nghệ và ứng dụng trí tuệ nhân tạo trong ngành tài chính.'''
    topic_list = topics.split('\n')
    topic_list = [topic.strip() for topic in topic_list if topic != '']
    return random.choice(topic_list)