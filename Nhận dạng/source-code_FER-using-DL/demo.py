import cv2
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from PIL import Image
from facenet_pytorch import MTCNN
from torchvision import transforms, models
from timm import create_model
from torchvision.models import ResNet50_Weights


###### Nhấn phím 'q' để thoát ######

# Có thể thay đổi đường dẫn đến mô hình đã huấn luyện để thử các mô hình khác
path_model = r'D:\AnChamHoc\CS338_Nhận dạng\Đồ án\source-code\models\fer2013.pth'

# --- SE Block ---
class SEBlock(nn.Module):
    def __init__(self, channel, reduction=16):
        super(SEBlock, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Sequential(
            nn.Linear(channel, channel // reduction, bias=False),
            nn.ReLU(inplace=True),
            nn.Linear(channel // reduction, channel, bias=False),
            nn.Sigmoid()
        )

    def forward(self, x): 
        b, c, _, _ = x.size()
        y = self.avg_pool(x).view(b, c)
        y = self.fc(y).view(b, c, 1, 1)
        return x * y.expand_as(x)

# --- Main Model ---
class SwinWithSEAndResNetFusion(nn.Module):
    def __init__(self, num_classes=7):
        super(SwinWithSEAndResNetFusion, self).__init__()
        self.swin_backbone = create_model('swin_tiny_patch4_window7_224', pretrained=True, features_only=True)
        self.resnet_backbone = models.resnet50(weights=ResNet50_Weights.DEFAULT)
        self.resnet_backbone = nn.Sequential(*list(self.resnet_backbone.children())[:-1])  
        self.se_block = SEBlock(768)
        self.split_conv = nn.Conv2d(768, 384, kernel_size=1)
        self.global_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(384 + 2048, num_classes)

    def forward(self, x):
        swin_feats = self.swin_backbone(x)[-1]           
        swin_feats = swin_feats.permute(0, 3, 1, 2)       
        swin_feats = self.se_block(swin_feats)
        swin_feats = self.split_conv(swin_feats)
        swin_feats = self.global_pool(swin_feats)
        swin_feats = swin_feats.flatten(1)               

        resnet_feats = self.resnet_backbone(x).flatten(1) 

        fused_feats = torch.cat([swin_feats, resnet_feats], dim=1)
        return self.fc(fused_feats)

# --- Load model ---
model = SwinWithSEAndResNetFusion(num_classes=7)
model.load_state_dict(torch.load(path_model, map_location=torch.device('cpu')))
model.eval()

# --- Emotion labels ---
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# --- Face detector ---
mtcnn = MTCNN(keep_all=True, device='cpu')

# --- Image preprocessing ---
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

# --- Open webcam ---
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes, _ = mtcnn.detect(img)

    if boxes is not None:
        for box in boxes:
            x1, y1, x2, y2 = map(int, box)
            face = img[y1:y2, x1:x2]

            if face.size == 0:
                continue  

            face_pil = Image.fromarray(face)
            face_tensor = transform(face_pil).unsqueeze(0)

            with torch.no_grad():
                output = model(face_tensor)
                probs = F.softmax(output, dim=1)
                pred = torch.argmax(probs, dim=1).item()
                label = emotion_labels[pred]

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    cv2.imshow('Emotion Recognition', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
