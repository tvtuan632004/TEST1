NHẬN DIỆN TÀU THUYỀN TỪ DỮ LIỆU VIỄN THÁM
PHẦN 1: TASK 1 - TIỀN XỬ LÝ DỮ LIỆU VỆ TÌNH
1. Mục tiêu
Chuyển đổi dữ liệu vệ tinh thô từ định dạng 16-bit sang 8-bit, thực hiện tổ hợp màu tự nhiên  và giữ nguyên hệ tọa độ tham chiếu (CRS) để phục vụ cho các bước phân tích không gian tiếp theo.

2. Quy trình kỹ thuật
Dữ liệu đầu vào: Ảnh vệ tinh đa phổ (.tif) kèm file metadata STAC JSON chứa thông tin các băng tần (Bands).

Tổ hợp màu tự nhiên: Trích xuất 3 kênh màu Red, Green, Blue dựa trên ánh xạ từ file JSON.

Kỹ thuật Stretch (Kéo dãn tương phản): Sử dụng phương pháp Percentile Stretch (2% - 98%) để loại bỏ các giá trị nhiễu và làm rõ nét hình ảnh.

Chuyển đổi 8-bit: Đưa dữ liệu về dải giá trị [0 - 255] để hiển thị trên các thiết bị dân dụng và tối ưu cho đầu vào của mô hình AI.

3. Kết quả đầu ra (Outputs)
Ảnh định dạng .tif: Lưu trữ dữ liệu 8-bit nhưng vẫn giữ nguyên hệ tọa độ CRS, đảm bảo tính chính xác về vị trí địa lý.

Ảnh định dạng .png: Bản xem trước (preview) phục vụ báo cáo và kiểm tra nhanh.

Tổ hợp màu tự nhiên: Hình ảnh tái hiện đúng màu sắc thực tế của khu vực cảng biển và tàu thuyền.

PHẦN 2: TASK 2 - HUẤN LUYỆN MÔ HÌNH NHẬN DIỆN (YOLOv8-OBB)
1. Cấu hình mô hình
Mô hình: YOLOv8s-OBB (Small - Oriented Bounding Box).

Đặc điểm: Sử dụng đa giác xoay thay vì hộp chữ nhật đứng để bao sát hình dáng tàu thuyền, giúp ước lượng chính xác hướng di chuyển.

2. Đánh giá kết quả (Metrics)
Dựa trên kết quả thực nghiệm sau 20 lượt huấn luyện (Epochs):

Precision (Độ chính xác): 0.71 (71%) - Khả năng nhận diện đúng đối tượng rất khả quan.

mAP50: 0.499 (~50%) - Mức độ chính xác trung bình đạt ngưỡng ổn định cho giai đoạn thử nghiệm.

Recall: 0.397 (~40%) - Hiện tại mô hình vẫn bỏ lỡ các tàu có kích thước quá nhỏ do độ phân giải đầu vào thấp.

3. Các yếu tố thúc đẩy sự cải thiện
Sức mạnh từ GPU & CUDA:

Việc có GPU cho phép thực hiện hàng nghìn phép tính song song, giúp mô hình hội tụ (convergence) sâu hơn. Với CPU, chúng ta buộc phải dừng ở 20 epoch để tiết kiệm thời gian, nhưng với GPU, việc chạy 200 - 300 epoch là khả thi, giúp mô hình tối ưu hóa các sai số nhỏ nhất.

Độ phân giải siêu cao (imgsz 1024+):

Trong ảnh vệ tinh, tàu thuyền thường chỉ chiếm một cụm pixel rất nhỏ. Khi tăng độ phân giải lên 1024, các đặc trưng của tàu (mũi tàu, cabin, hướng xoay) sẽ trở nên sắc nét. Điều này trực tiếp giải quyết vấn đề Recall thấp, giúp mô hình không bỏ sót bất kỳ đối tượng nào dù là nhỏ nhất.

Dataset đa dạng và chất lượng cao:

Sử dụng dataset lớn hơn (ví dụ: bổ sung thêm dữ liệu từ các vùng biển, điều kiện ánh sáng và thời tiết khác nhau) sẽ giúp mô hình tăng khả năng Tổng quát hóa (Generalization). Mô hình sẽ không còn bị nhầm lẫn bởi bọt sóng, mây che hay bóng đổ từ cầu cảng.

Kiến trúc mô hình lớn hơn (Large/X-Large):

Với GPU, chúng ta có thể sử dụng các bản mô hình yolov8l-obb hoặc yolov8x-obb. Các mạng thần kinh sâu hơn này có khả năng trích xuất các đặc trưng hình học cực kỳ phức tạp, đưa độ chính xác (Precision) tiệm cận mức tuyệt đối.

4. Kết luận và Hướng phát triển
Đánh giá chung: Mặc dù huấn luyện trong điều kiện "Model trung bình + Phần cứng yếu", hệ thống đã đạt được các chỉ số cơ bản để chứng minh tính khả thi của giải pháp.
