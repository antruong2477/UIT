import cv2
import os
import torch
from torchvision import transforms
from PIL import Image, ImageDraw
import numpy as np
import time # Để tính FPS (tùy chọn)


# MODEL_PATH = "./face_localization_model.pth"

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'face_localization_model.pth')

from model import FaceLocalizationModel  


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

print("Loading model...")

model = FaceLocalizationModel()


try:
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device, weights_only=True))
except TypeError:
 
    print("Warning: PyTorch version might be older. Loading without weights_only=True. Ensure the model file is trusted.")
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
except Exception as e:
    print(f"Error loading model weights: {e}")
    print("Please ensure MODEL_PATH is correct and the model definition matches the saved weights.")
    exit()

model.to(device)
model.eval() 
print("Model loaded successfully.")


INPUT_SIZE = 224 
inference_transform = transforms.Compose([
    transforms.Resize((INPUT_SIZE, INPUT_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# ----- KHỞI TẠO CAMERA -----
print("Initializing camera...")
cap = cv2.VideoCapture(0) 
if not cap.isOpened():
    print("Lỗi: Không thể mở camera. Kiểm tra lại camera hoặc index.")
    exit()

print("Camera initialized. Press 'q' to quit.")


prev_time = 0 
while True:

    ret, frame = cap.read()
    if not ret:
        print("Lỗi: Không thể đọc frame từ camera.")
        break


    original_height, original_width = frame.shape[:2]

  
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_frame)

    input_tensor = inference_transform(pil_image).unsqueeze(0).to(device)


    with torch.no_grad():
        output = model(input_tensor)


    predicted_box_resized = output.cpu().numpy()[0]
    xmin_res, ymin_res, xmax_res, ymax_res = predicted_box_resized

 
    width_scale = original_width / INPUT_SIZE
    height_scale = original_height / INPUT_SIZE


    xmin_orig = int(xmin_res * width_scale)
    ymin_orig = int(ymin_res * height_scale)
    xmax_orig = int(xmax_res * width_scale)
    ymax_orig = int(ymax_res * height_scale)


    xmin_orig = max(0, xmin_orig)
    ymin_orig = max(0, ymin_orig)
    xmax_orig = min(original_width - 1, xmax_orig)
    ymax_orig = min(original_height - 1, ymax_orig)

 
    box_width = xmax_orig - xmin_orig
    box_height = ymax_orig - ymin_orig
    if box_width > 10 and box_height > 10: # Ngưỡng kích thước tối thiểu (có thể điều chỉnh)
       cv2.rectangle(frame, (xmin_orig, ymin_orig), (xmax_orig, ymax_orig), (0, 255, 0), 2) # Màu xanh lá, độ dày 2

    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time
    cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow('Real-time Face Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exiting...")
        break

# ----- Giải phóng tài nguyên -----
cap.release()
cv2.destroyAllWindows()
print("Resources released.")
