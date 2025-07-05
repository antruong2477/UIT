import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms
from torch.utils.data import DataLoader
from dataset import FaceLocalizationDataset  # Import Dataset từ dataset.py
from model import FaceLocalizationModel      # Import Model từ model.py
from sklearn.model_selection import train_test_split # Import để chia dữ liệu
import os

# Đường dẫn đến thư mục ảnh và JSON (CẦN THAY ĐỔI)
IMAGE_DIR = 'E:/UIT/CS331/week7/data'
JSON_DIR = 'E:/UIT/CS331/week7/json'
MODEL_PATH = 'face_localization_model.pth' # Đường dẫn lưu model

# Hyperparameters
BATCH_SIZE = 4
LEARNING_RATE = 1e-5
NUM_EPOCHS = 50
VAL_SIZE = 0.15 
TEST_SIZE = 0.15 


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

all_image_files = [f for f in os.listdir(IMAGE_DIR) if os.path.isfile(os.path.join(IMAGE_DIR, f))]

train_files, val_test_files = train_test_split(all_image_files, test_size=(VAL_SIZE + TEST_SIZE), random_state=42) 

val_files, test_files = train_test_split(val_test_files, test_size=TEST_SIZE / (VAL_SIZE + TEST_SIZE) if (VAL_SIZE + TEST_SIZE) > 0 else 0, random_state=42) 

print(f"Number of training files: {len(train_files)}")
print(f"Number of validation files: {len(val_files)}")
print(f"Number of test files: {len(test_files)}")

train_dataset = FaceLocalizationDataset(train_files, IMAGE_DIR, JSON_DIR, transform=transform)
val_dataset = FaceLocalizationDataset(val_files, IMAGE_DIR, JSON_DIR, transform=transform)
train_dataloader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_dataloader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False) # shuffle=False cho validation

model = FaceLocalizationModel().to(device)

criterion = nn.MSELoss()

optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

def evaluate_model(model, dataloader, criterion, device):
    model.eval()
    total_loss = 0.0
    with torch.no_grad():
        for data in dataloader:
            inputs, boxes = data
            inputs, boxes = inputs.to(device), boxes.to(device)
            outputs = model(inputs)
            outputs = outputs.view(-1, 1, 4)
            loss = criterion(outputs, boxes)
            total_loss += loss.item()
    avg_loss = total_loss / len(dataloader)
    return avg_loss

print("Starting Training...")
best_val_loss = float('inf') 
for epoch in range(NUM_EPOCHS):
    running_loss = 0.0
    for i, data in enumerate(train_dataloader, 0):
        inputs, boxes = data
        inputs, boxes = inputs.to(device), boxes.to(device)

        optimizer.zero_grad()

        outputs = model(inputs)
        outputs = outputs.view(-1, 1, 4)

        loss = criterion(outputs, boxes)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        if i % 10 == 9:
            print(f'[{epoch + 1}, {i + 1:5d}] loss: {running_loss / 10:.3f}')
            running_loss = 0.0

    # Đánh giá trên validation set sau mỗi epoch
    val_loss = evaluate_model(model, val_dataloader, criterion, device)
    print(f'Epoch {epoch+1} Validation Loss: {val_loss:.4f}')

    # Lưu model tốt nhất dựa trên validation loss
    if val_loss < best_val_loss:
        best_val_loss = val_loss
        torch.save(model.state_dict(), MODEL_PATH)
        print(f'Model saved at epoch {epoch+1} with Validation Loss: {best_val_loss:.4f}')

print('Finished Training')
print(f'Best Validation Loss: {best_val_loss:.4f}')
print(f'Best Model saved to {MODEL_PATH}')