"""
Bài làm tách riêng các đặc trưng 
CS231.P11: Bài tập thực hành 01
MSSV: 22520033
Họ và tên: Trương Huỳnh Thúy An
"""

from scipy.spatial import distance
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from scipy.stats import skew, kurtosis
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import cv2
import os

bin_size = 8

def create_image_label_dataframe(dir_path): 
    root_dir = os.listdir(dir_path)
    images = []
    labels = []
    for subfolder in root_dir: 
        subfolder_path = os.path.join(dir_path, subfolder)
        if not os.path.isdir(subfolder_path) or subfolder == 'train':
            continue
        for image_filename in os.listdir(subfolder_path):
            image_path = os.path.join(subfolder_path, image_filename)
            images.append(image_path)
            labels.append(subfolder)
        
    df = pd.DataFrame({'image': images, 'label': labels})
    return df

def read_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2LUV)
    return image

def normalize_feature(feature):
    norm = np.linalg.norm(feature)
    if norm == 0:
        return feature
    return feature / norm

####### Các hàm trích xuất đặc trưng #######
def normalized_color_histogram(image):
    row, column, channel = image.shape[:3]
    size = row * column
    
    feature = []
    for k in range(channel):
        histogram = cv2.calcHist([image], [k], None, [bin_size], [0, 256])
        histogram = histogram / size
        feature.extend(histogram.flatten())
    return feature

def moment(channel):
    feature = []
    mean_value = np.mean(channel)
    std_value = np.std(channel)
    
    if std_value == 0:
        feature.append(mean_value)
        feature.append(std_value)
        feature.append(0)
        feature.append(0)
    else:
        feature.append(mean_value)
        feature.append(std_value)
        feature.append(skew(channel))
        feature.append(kurtosis(channel))
    
    return feature

def extract_color_moment(image):
    row, column, channel = image.shape[:3]
    
    channel_list = [[] for _ in range(channel)]
    
    for i in range(row):
        for j in range(column):
            for k in range(channel):
                channel_list[k].append(image[i][j][k])
    
    feature = []
    for i in range(channel):
        feature.extend(moment(channel_list[i]))
    
    return feature

def DCD(image, k=3):
    image = cv2.cvtColor(image, cv2.COLOR_LUV2BGR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    pixels = image.reshape(-1, 3)

    kmeans = KMeans(n_clusters=k)
    kmeans.fit(pixels)

    dominant_colors = kmeans.cluster_centers_.astype(int)
    dominant_ratios = np.bincount(kmeans.labels_) / len(kmeans.labels_)

    feature = []
    for i in range(len(dominant_ratios)):
        color = list(normalize_feature(dominant_colors[i]))
        ratio = dominant_ratios[i]
        feature.extend(color)
        feature.append(ratio)

    while len(feature) != 12:
        feature.append(0)
    return feature

def ccv(image, t=50):
    row, col, ch = image.shape
    ccv_feature = []
    for i in range(ch):
        channel = image[:, :, i]
        hist, _ = np.histogram(channel, bins=256, range=(0, 256))
        coherent = np.sum(hist[hist >= t])
        incoherent = np.sum(hist[hist < t])
        ccv_feature.append(coherent)
        ccv_feature.append(incoherent)
    return ccv_feature

### Các hàm tính khoảng cách ###
def intersection_distance(x, y):
    return 1 - np.sum(np.minimum(x, y))

def bhattacharyya_distance(x, y):
    x = x / np.sum(x) if np.sum(x) > 0 else x
    y = y / np.sum(y) if np.sum(y) > 0 else y
    return -np.log(np.sum(np.sqrt(x * y)) + 1e-10)

def chi_square_distance(x, y):
    return 0.5 * np.sum(((x - y) ** 2) / (x + y + 1e-10)) 

###  ###
def extract_features(dataframe, feature_extractor):
    x = []
    y = []
    for image, label in zip(dataframe['image'], dataframe['label']):
        image = read_image(image)
        features = feature_extractor(image)
        x.append(features)
        y.append(label)
    return x, y

def main():
    train_df = create_image_label_dataframe('train')
    test_df = create_image_label_dataframe('test')
    
    distance_metrics = {
        'euclidean':  'euclidean',
        'correlation': 'correlation',
        'chi-square': chi_square_distance,
        'intersection': intersection_distance,
        'bhattacharyya': bhattacharyya_distance
    }
    
    extractor = {
        'color_histogram': normalized_color_histogram,
        'color_moment': extract_color_moment,
        'dcd': DCD,
        'ccv': ccv
    }
    print_result = []
    for feature_name, extract_feature in extractor.items():
        print_result.append(f'Extracting features with {feature_name}')
        x_train, y_train = extract_features(train_df, extract_feature)
        x_test, y_test = extract_features(test_df, extract_feature)
        
        scaler = MinMaxScaler()
        x_train = scaler.fit_transform(x_train)
        x_test = scaler.transform(x_test)
        
        for k in [1, 5]:    
            print_result.append(f'With k = {k}') 
            for metric_name, metric in distance_metrics.items():
                model = KNeighborsClassifier(n_neighbors=k, metric=metric)
                model.fit(x_train, y_train)
                y_pred = model.predict(x_test)
                accuracy = accuracy_score(y_test, y_pred)
                print_result.append(f'Metric {metric_name}: accuracy = {accuracy}')
            print_result.append('-----------------------------------------')
        print_result.append("____________________________________________________________________")

    print('=========================================================================================')
    print('\n'.join(print_result))
    
if __name__ == "__main__":
    main()
