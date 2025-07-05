import torch
from torchvision import transforms
from PIL import Image, ImageDraw
from model import FaceLocalizationModel # Import model từ model.py

# Đường dẫn đến model đã huấn luyện (CẦN ĐẢM BẢO ĐÚNG)
MODEL_PATH = 'face_localization_model.pth'
# Đường dẫn đến ảnh bạn muốn test (CẦN THAY ĐỔI)
IMAGE_PATH = 'E:/UIT/CS331/week7/data/image_005.jpg'
# Đường dẫn lưu ảnh kết quả (bounding box vẽ trên ảnh gốc)
OUTPUT_IMAGE_PATH = 'output_image_with_bbox.jpg'

# Load model đã huấn luyện
loaded_model = FaceLocalizationModel()
loaded_model.load_state_dict(torch.load(MODEL_PATH))
loaded_model.eval() # Chuyển sang chế độ evaluation

# Thiết bị (CPU cho demo, có thể dùng GPU nếu cần)
device = torch.device("cpu")
loaded_model.to(device)

# Transform ảnh cho inference (giống transform khi training)
inference_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Mở ảnh bằng PIL
pil_image = Image.open(IMAGE_PATH).convert('RGB')
original_width, original_height = pil_image.size # Lấy kích thước gốc

# Áp dụng transform và thêm batch dimension
input_tensor = inference_transform(pil_image).unsqueeze(0).to(device)

# Inference
with torch.no_grad():
    output = loaded_model(input_tensor)

# Lấy bounding box dự đoán từ output model
predicted_box = output.cpu().numpy()[0]

# Chuyển đổi tọa độ bounding box về kích thước gốc của ảnh
x_min_resized = predicted_box[0]
y_min_resized = predicted_box[1]
x_max_resized = predicted_box[2]
y_max_resized = predicted_box[3]

# Tính toán tọa độ bounding box trên ảnh gốc (inverse resize)
resized_width = 224
resized_height = 224
width_ratio = resized_width / original_width
height_ratio = resized_height / original_height

x_min_original = int(x_min_resized / width_ratio)
y_min_original = int(y_min_resized / height_ratio)
x_max_original = int(x_max_resized / width_ratio)
y_max_original = int(y_max_resized / height_ratio)


# Vẽ bounding box lên ảnh gốc bằng PIL
draw = ImageDraw.Draw(pil_image)
draw.rectangle([(x_min_original, y_min_original), (x_max_original, y_max_original)], outline="green", width=2) # Màu xanh lá cây, độ dày 2

# Lưu ảnh kết quả
pil_image.save(OUTPUT_IMAGE_PATH)
print(f"Ảnh với bounding box đã được lưu tại: {OUTPUT_IMAGE_PATH}")

# (Tùy chọn) Hiển thị ảnh kết quả (yêu cầu có thư viện matplotlib)
# import matplotlib.pyplot as plt
# plt.imshow(pil_image)
# plt.show()