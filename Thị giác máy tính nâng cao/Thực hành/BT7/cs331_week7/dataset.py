import torch
from torch.utils.data import Dataset
from torchvision import transforms
from PIL import Image
import json
import os

class FaceLocalizationDataset(Dataset):
    def __init__(self, image_files, image_dir, json_dir, transform=None):
        self.image_files = image_files
        self.image_dir = image_dir
        self.json_dir = json_dir
        self.transform = transform

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        img_name = self.image_files[idx]
        img_path = os.path.join(self.image_dir, img_name)
        json_name = os.path.splitext(img_name)[0] + '.json'
        json_path = os.path.join(self.json_dir, json_name)

        image = Image.open(img_path).convert('RGB')
        original_width, original_height = image.size # Lấy kích thước ảnh gốc
        with open(json_path, 'r') as f:
            json_data = json.load(f)

        boxes = torch.tensor([[0, 0, 0, 0]], dtype=torch.float32)
        if json_data['shapes']:
            for shape in json_data['shapes']:
                if shape['label'] == 'face':
                    points = shape['points']
                    x_min = int(points[0][0])
                    y_min = int(points[0][1])
                    x_max = int(points[1][0])
                    y_max = int(points[1][1])

            
                    resized_width = 224
                    resized_height = 224
                    width_ratio = resized_width / original_width
                    height_ratio = resized_height / original_height


                    x_min_resized = int(x_min * width_ratio)
                    y_min_resized = int(y_min * height_ratio)
                    x_max_resized = int(x_max * width_ratio)
                    y_max_resized = int(y_max * height_ratio)
                    boxes_resized = torch.tensor([[x_min_resized, y_min_resized, x_max_resized, y_max_resized]], dtype=torch.float32)
                    boxes = boxes_resized # Gán boxes đã resize

                    break

        if self.transform:
            image = self.transform(image)

        return image, boxes # Trả về boxes đã resize
if __name__ == '__main__':

    image_dir = 'path/to/your/image/folder'
    json_dir = 'path/to/your/json/folder'

    all_image_files = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]

    train_files = all_image_files[:int(0.7 * len(all_image_files))]
    val_files = all_image_files[int(0.7 * len(all_image_files)):int(0.9 * len(all_image_files))]
    test_files = all_image_files[int(0.9 * len(all_image_files)):]

    # Transform ảnh
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    # Tạo Dataset cho train, val, test
    train_dataset = FaceLocalizationDataset(train_files, image_dir, json_dir, transform=transform)
    val_dataset = FaceLocalizationDataset(val_files, image_dir, json_dir, transform=transform)
    test_dataset = FaceLocalizationDataset(test_files, image_dir, json_dir, transform=transform)

    # Kiểm tra Dataset (lấy mẫu đầu tiên từ train)
    sample_image, sample_boxes = train_dataset[0]
    print("Sample train image shape:", sample_image.shape)
    print("Sample train boxes:", sample_boxes)

    # Tạo DataLoader để kiểm tra batching (cho train)
    from torch.utils.data import DataLoader
    train_dataloader = DataLoader(train_dataset, batch_size=4, shuffle=True)
    for images, boxes in train_dataloader:
        print("Train Image batch shape:", images.shape)
        print("Train Boxes batch shape:", boxes.shape)
        print("Sample train batch boxes:", boxes)
        break