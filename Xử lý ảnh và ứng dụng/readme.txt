# Tài liệu Dự án Phát hiện Mũ Bảo hiểm

## 1. Thành viên Nhóm

- Trương Huỳnh Thúy An - Mã số sinh viên: 22520033
- Trương Hồng Anh - Mã số sinh viên: 22520084
- Hoàng Đức Chung - Mã số sinh viên: 22520161
- Nguyễn Hải Đăng - Mã số sinh viên: 22520189

## 2. Hướng dẫn Cài đặt và Chạy Mã

Để cài đặt và chạy ứng dụng phát hiện mũ bảo hiểm, hãy làm theo các bước sau:

1. Cài đặt các thư viện cần thiết bằng lệnh sau:
        "pip install -r requirements.txt"
    
2. Chạy ứng dụng web Streamlit bằng lệnh sau:
        "streamlit run streamlit_cs406.py"

Ứng dụng sẽ mở trong trình duyệt web mặc định.

3. Sử dụng ứng dụng:
- Chọn ảnh hoặc video để kiểm thử.
- Điều chỉnh độ tin cậy phát hiện bằng thanh trượt.
- Có ô chọn "Select Prediction Method":
    + Single YOLO model: Có thể chọn 3 phiên bản YOLOv5m, YOLOv8m và YOLO11m để kiểm tra.
    + Combined YOLO Models with WBF: Trọng số để kết hợp cho từng mô hình đã được thiết lập cố định.
    + SAHI: SAHI mới hỗ trợ cho YOLOv5 và YOLOv8, trong đó đã thiết lập để thực hiện kiểm tra YOLOv8m với SAHI.
- Sau khi chọn xong chỉ cần nhấn nút "Run Prediction".

## 3. Truy cập Ứng dụng Web Đã Triển khai

- CCó thể truy cập ứng dụng web đã triển khai tại liên kết sau:
https://prj-cs406.streamlit.app/?fbclid=IwY2xjawHLu3xleHRuA2FlbQIxMAABHXfMiD84SWapgxh8Q1Bvhwqpjrnbv2_gHV1yWPZ4ovGCbQ8SvgivH0nFvA_aem_qbGu-Mgz3zpOiKT6NbDxWg

## 4. Liên kết Dataset

- Dataset sử dụng cho dự án có tại:
https://www.kaggle.com/datasets/truonghonganh/cs406-dataset