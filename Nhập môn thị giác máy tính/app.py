import streamlit as st
import pickle
import cv2
import numpy as np
from skimage import feature  
import joblib
from skimage import filters
import os

# 1. Load model từ file pkl
@st.cache_resource  
def load_model(model_path):
    """Tải model từ đường dẫn đã chỉ định"""
    best_model = joblib.load(model_path)
    return best_model

# 2.a Các hàm tính đặc trưng cho Prewitt, Sobel và HOG
def compute_hog_single(image):
    """Tính đặc trưng HOG từ ảnh đầu vào"""
    img_resized = cv2.resize(image, (128, 128))
    hog_feature = feature.hog(
        img_resized, 
        orientations=9,
        pixels_per_cell=(8, 8),
        cells_per_block=(2, 2),
        block_norm='L2',
        visualize=False,
        transform_sqrt=True)
    return hog_feature

def compute_hog_arg_single(image):
    """Tính đặc trưng HOG từ ảnh đầu vào"""
    img_resized = cv2.resize(image, (128, 128))
    hog_feature = feature.hog(
        img_resized, 
        orientations=9,
        pixels_per_cell=(10, 10),
        cells_per_block=(2, 2),
        block_norm='L2',
        visualize=False,
        transform_sqrt=True)
    return hog_feature

def compute_prewitt_features(image):
    """Tính đặc trưng Prewitt từ ảnh đầu vào"""
    image = cv2.resize(image, (128, 128))
    prewitt_h_edges = filters.prewitt_h(image)
    prewitt_v_edges = filters.prewitt_v(image)
    prewitt_edges = np.sqrt(prewitt_h_edges**2 + prewitt_v_edges**2)
    return prewitt_edges.flatten()

def compute_sobel_features(image):
    """Tính đặc trưng Sobel từ ảnh đầu vào"""
    img_resized = cv2.resize(image, (128, 128))
    smoothed_image = cv2.GaussianBlur(img_resized, (3, 3), 0)
    sobel_x = cv2.Sobel(smoothed_image, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(smoothed_image, cv2.CV_64F, 0, 1, ksize=3)
    gradient_mag = np.sqrt(sobel_x**2 + sobel_y**2)
    return gradient_mag.flatten()

# 3. Hàm dự đoán chữ số từ hình ảnh
def predict_image(model, image, decorator_type):
    """Dự đoán chữ số từ ảnh đầu vào sử dụng model"""
    if decorator_type == "Prewitt":
        features = compute_prewitt_features(image)
    elif decorator_type == "Sobel":
        features = compute_sobel_features(image)
    elif decorator_type == "HOG":
        features = compute_hog_single(image)
    elif decorator_type == "HOG_with_arg":
        features = compute_hog_arg_single(image)
    
    processed_image = features.reshape(1, -1) 
    prediction = model.predict(processed_image)
    return int(prediction[0])

# 4. Giao diện người dùng
def main():
    st.title("Nhận diện ngôn ngữ ký hiệu (0-9) từ hình ảnh bàn tay")
    st.write("Hãy tải lên một hoặc nhiều hình ảnh (các ảnh có thể là chữ số 0-9 từ ngôn ngữ ký hiệu)")

    # Chọn loại bộ lọc
    decorator = st.selectbox("Chọn loại bộ lọc", ["Prewitt", "Sobel", "HOG", "HOG_with_arg"])
    model_path = f"Models/svm_{decorator.lower()}_model.pkl"
    if not os.path.exists(model_path):
        st.error(f"Không tìm thấy file model: {model_path}")
        return
    
    model = load_model(model_path)
    st.success(f"Model svm with {decorator} đã được tải thành công!")

    # Người dùng tải lên ảnh
    uploaded_files = st.file_uploader("Chọn các ảnh cần dự đoán", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)
    
    if uploaded_files:
        predicted_numbers = []
        images = []

        for uploaded_file in uploaded_files:
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            image_color = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            image_color = cv2.cvtColor(image_color, cv2.COLOR_BGR2RGB)

            image = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE) 
            if image is None:
                st.error(f"Không thể đọc ảnh từ file {uploaded_file.name}.")
                continue
            
            # Dự đoán số từ ảnh
            try:
                predicted_number = predict_image(model, image, decorator)
                predicted_numbers.append(str(predicted_number))
                images.append(image_color)
            except Exception as e:
                st.error(f"Không thể dự đoán ảnh này. Lỗi: {e}")
        
        # Hiển thị các ảnh theo hàng và cột
        if images:
            st.subheader("Các ảnh đã tải lên và kết quả dự đoán:")
            rows = len(images) // 5 + (1 if len(images) % 5 != 0 else 0)  # Tính số hàng cần hiển thị
            for i in range(rows):
                start_idx = i * 5
                end_idx = min((i + 1) * 5, len(images))
                cols = st.columns(end_idx - start_idx)
                for j, img in enumerate(images[start_idx:end_idx]):
                    cols[j].image(img, caption=f"Ảnh {start_idx + j + 1}", width=100)  # Hiển thị ảnh nhỏ

        # Hiển thị kết quả cuối cùng
        if predicted_numbers:
            phone_number = ' '.join(predicted_numbers)
            st.subheader(f"Số điện thoại của bạn có phải là: **{phone_number}**")
        
if __name__ == "__main__":
    main()
