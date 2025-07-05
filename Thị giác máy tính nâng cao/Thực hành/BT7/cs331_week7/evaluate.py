import torch
import torch.nn as nn
from torchvision import transforms
from torch.utils.data import DataLoader
from dataset import FaceLocalizationDataset
from model import FaceLocalizationModel
from sklearn.model_selection import train_test_split 
import os


IMAGE_DIR = r'D:\AnChamHoc\CS331_Thị giác máy tính nâng cao\Thực Hành\BT7\cs331_week7\data'
JSON_DIR = r'D:\AnChamHoc\CS331_Thị giác máy tính nâng cao\Thực Hành\BT7\cs331_week7\json'
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'face_localization_model.pth')

BATCH_SIZE = 4
VAL_SIZE = 0.15 
TEST_SIZE = 0.15 

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

test_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])


all_image_files = [f for f in os.listdir(IMAGE_DIR) if os.path.isfile(os.path.join(IMAGE_DIR, f))]
train_files, val_test_files = train_test_split(all_image_files, test_size=(VAL_SIZE + TEST_SIZE), random_state=42)
val_files, test_files = train_test_split(val_test_files, test_size=TEST_SIZE / (VAL_SIZE + TEST_SIZE) if (VAL_SIZE + TEST_SIZE) > 0 else 0, random_state=42)


test_dataset = FaceLocalizationDataset(test_files, IMAGE_DIR, JSON_DIR, transform=test_transform)
test_dataloader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False) # shuffle=False cho test


model = FaceLocalizationModel().to(device)
model.load_state_dict(torch.load(MODEL_PATH)) 

criterion = nn.MSELoss()


def calculate_iou(box1, box2):
    """Tính IoU của hai bounding box [x_min, y_min, x_max, y_max]."""
    x_min_inter = max(box1[0], box2[0])
    y_min_inter = max(box1[1], box2[1])
    x_max_inter = min(box1[2], box2[2])
    y_max_inter = min(box1[3], box2[3])

    inter_area = max(0, x_max_inter - x_min_inter) * max(0, y_max_inter - y_min_inter)
    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])
    union_area = box1_area + box2_area - inter_area
    return inter_area / union_area if union_area > 0 else 0
def evaluate_model(model, dataloader, criterion, device, iou_threshold=0.5):
    """
    Đánh giá model trên dataloader, tính loss và mAP (simplified).

    Args:
        model (nn.Module): Model cần đánh giá.
        dataloader (DataLoader): DataLoader cho validation hoặc test dataset.
        criterion (nn.Module): Hàm loss (ví dụ: MSELoss).
        device (torch.device): Thiết bị tính toán (CPU hoặc GPU).
        iou_threshold (float): Ngưỡng IoU để coi là True Positive (TP).

    Returns:
        tuple: (avg_loss, mAP) - loss trung bình và mAP.
    """
    model.eval()
    total_loss = 0.0
    true_positives = 0
    false_positives = 0
    false_negatives = 0

    with torch.no_grad():
        for data in dataloader:
            inputs, target_boxes_batch = data # target_boxes_batch là ground truth boxes
            inputs, target_boxes_batch = inputs.to(device), target_boxes_batch.to(device)

            outputs_batch = model(inputs)
            outputs_batch = outputs_batch.view(-1, 1, 4) # Reshape output

            loss = criterion(outputs_batch, target_boxes_batch)
            total_loss += loss.item()

            # Chuyển bounding box dự đoán và ground truth về CPU và numpy array
            predicted_boxes_batch_cpu = outputs_batch.cpu().numpy()
            target_boxes_batch_cpu = target_boxes_batch.cpu().numpy()

            # Lặp qua từng ảnh trong batch
            for i in range(inputs.size(0)): # inputs.size(0) là batch size
                predicted_box = predicted_boxes_batch_cpu[i][0] # Lấy bounding box dự đoán cho ảnh thứ i
                target_box = target_boxes_batch_cpu[i][0]     # Lấy bounding box ground truth cho ảnh thứ i

                # Tính IoU giữa bounding box dự đoán và ground truth
                iou = calculate_iou(predicted_box, target_box)

                if target_box.sum() == 0: # Nếu ground truth là [0, 0, 0, 0] (không có face)
                    if predicted_box.sum() != 0: # Model dự đoán có face (FP)
                        false_positives += 1
                    # Nếu model cũng dự đoán không có face (TN), không tính vào TP, FP, FN
                else: # Nếu có ground truth face
                    if iou >= iou_threshold: # IoU đủ lớn (TP)
                        true_positives += 1
                    else: # IoU không đủ lớn (FP)
                        false_positives += 1 # Coi dự đoán IoU thấp là False Positive
                        # false_negatives không cần tăng ở đây nữa

    avg_loss = total_loss / len(dataloader)

    # Tính Precision, Recall, mAP (simplified)
    precision = true_positives / (true_positives + false_positives + 1e-6) # Thêm epsilon để tránh chia cho 0
    recall = true_positives / (true_positives + false_negatives + 1e-6) # FN có thể cần được tính toán khác nếu cần độ chính xác cao hơn
    f1_score = 2 * (precision * recall) / (precision + recall + 1e-6) # Tính F1-score
    mAP = f1_score # Hoặc mAP = precision nếu muốn đơn giản hơn

    return avg_loss, mAP, precision, recall, f1_score
# Đánh giá model trên test set
print("Starting Evaluation on Test Set...")
test_loss = evaluate_model(model, test_dataloader, criterion, device)
print(f'Test Loss: {test_loss}')
print("Evaluation Finished.")