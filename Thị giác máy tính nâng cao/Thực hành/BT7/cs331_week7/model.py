import torch
import torch.nn as nn
import torch.nn.functional as F

class FaceLocalizationModel(nn.Module):
    def __init__(self):
        super(FaceLocalizationModel, self).__init__()

        self.conv1 = self.create_conv_block(3, 16, kernel_size=3) 
        self.conv2 = self.create_conv_block(16, 32, kernel_size=3)
        self.conv3 = self.create_conv_block(32, 64, kernel_size=3)
        self.conv4 = self.create_conv_block(64, 128, kernel_size=3)
        self.conv5 = self.create_conv_block(128, 256, kernel_size=3)


        fc_input_size = 256 * 7 * 7

        self.fc1 = nn.Sequential(
            nn.Linear(fc_input_size, 1024), 
            nn.ReLU(),
            nn.Dropout(0.5)
        )
        self.fc2 = nn.Sequential(
            nn.Linear(1024, 512),         
            nn.ReLU(),
            nn.Dropout(0.5)
        )
        # self.fc3 = nn.Sequential(       # Có thể bỏ bớt 1 lớp FC nếu cần
        #     nn.Linear(512, 256),
        #     nn.ReLU()
        # )
        self.fc_output = nn.Linear(512, 4) 

    def create_conv_block(self, input_channels, output_channels, kernel_size=3):
        padding = kernel_size // 2 
        return nn.Sequential(
            nn.Conv2d(input_channels, output_channels, kernel_size=kernel_size, padding=padding),
            nn.BatchNorm2d(output_channels), 
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.conv4(x)
        x = self.conv5(x)
        # print("Shape after conv5:", x.shape) # Debug để kiểm tra shape
        x = x.view(x.size(0), -1) # Flatten
        x = self.fc1(x)
        x = self.fc2(x)
        # x = self.fc3(x) # Nếu sử dụng fc3
        x = self.fc_output(x)
        return x