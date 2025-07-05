#MSSV : 22520069
#Ho va ten : Pham Nguyen Anh

import numpy as np
import cv2
import os
import sys
from scipy.stats import skew, kurtosis
from scipy.spatial import distance
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
from sklearn.cluster import KMeans
from sklearn import metrics
from tqdm import tqdm
from sklearn.preprocessing import normalize

BIN_SIZE = 16
TEST_PATH = 'test'
TRAIN_PATH = 'train'

def read_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2LUV)
    return image

def normalize_vector(feature):
    norm = np.linalg.norm(feature)
    if norm == 0:
        return feature
    return feature / norm

def normalized_color_histogram(image):
    row, column, channel = image.shape[:3]
    size = row * column
    
    feature = []
    for k in range(channel):
        histogram = cv2.calcHist([image], [k], None, [BIN_SIZE], [0, 256])
        histogram = histogram / size
        feature.extend(histogram.flatten())
    return feature

def moment(channel):
    feature = []    
    feature.append(np.mean(channel))
    feature.append(np.std(channel))
    feature.append(skew(channel))
    feature.append(kurtosis(channel))
    return feature


def color_moment(image):
    row, column, channel = image.shape[:3]
    
    channel_list = []
    for i in range(channel):
        channel_list.append([])
    
    for i in range(row):
        for j in range(column):
            for k in range(channel):
                channel_list[k].append(image[i][j][k])
    
    feature = []
    for i in range(channel):
        feature.extend(moment(channel_list[i]))
    
    return feature

def normalize_moment_feature(data, str_point, number_of_channel):
    # 4 : number of color moment feature
    end_point = str_point + number_of_channel * 4
    
    number_of_data = len(data)
    for i in range(str_point, end_point):
        min_val = sys.maxsize
        max_val = 0
        for j in range(number_of_data):
            if data[j][i] < min_val:
                min_val = data[j][i]
            if data[j][i] > max_val:
                max_val = data[j][i]
        
        # min - max normalization
        for j in range(number_of_data):
            data[j][i] = (data[j][i] - min_val) / (max_val - min_val)

def cdc(image):
    # Lấy vùng trung tâm của ảnh
    center = image[image.shape[0]//4:3*image.shape[0]//4, image.shape[1]//4:3*image.shape[1]//4]
    return np.mean(center, axis=(0, 1))

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


# def ccv(image):
#     feature = []
#     for k in range(image.shape[2]):
#         channel_data = image[:, :, k].flatten()
#         feature.append(np.sum(channel_data > 0))
#     return feature

# def ccv(image):
#     feature = []
#     total_pixels = image.shape[0] * image.shape[1]
    
#     for k in range(image.shape[2]):
#         channel_data = image[:, :, k].flatten()
        
#         # Tính số lượng pixel dương
#         positive_count = np.sum(channel_data > 0)
        
#         # Tính số lượng pixel không dương
#         non_positive_count = total_pixels - positive_count
        
#         # Tính tỷ lệ pixel dương
#         feature.append(positive_count / total_pixels)
#         # Tính tỷ lệ pixel không dương
#         feature.append(non_positive_count / total_pixels)

#     return feature

def euclidean_distance(x, y):
    return distance.euclidean(x, y)

def correlation_distance(x, y):
    return 1 - np.corrcoef(x, y)[0, 1]

def intersection_distance(x, y):
    return 1 - np.sum(np.minimum(x, y))

def bhattacharyya_distance(x, y):
    x = x / np.sum(x) if np.sum(x) > 0 else x
    y = y / np.sum(y) if np.sum(y) > 0 else y
    return -np.log(np.sum(np.sqrt(x * y)) + 1e-10)

def chi_square_distance(x, y):
    return np.sum((x - y) ** 2 / (x + y + 1e-10)) 

if __name__ == '__main__':
    distance_metrics = {
        'chi-square': chi_square_distance,
        'euclidean': euclidean_distance,
        'correlation': correlation_distance,
        'intersection': intersection_distance,
        'bhattacharyya': bhattacharyya_distance
    }

    number_of_train_image_count = 0
    color_list = os.listdir(TRAIN_PATH)
    for index, color_name in enumerate(color_list):
        path = os.path.join(TRAIN_PATH, color_name)
        image_list = os.listdir(os.path.join(path))
        for image_name in image_list:
            number_of_train_image_count += 1
            
    # find number of test images
    number_of_test_image_count = 0
    color_list = os.listdir(TEST_PATH)
    for index, color_name in enumerate(color_list):
        path = os.path.join(TEST_PATH, color_name)
        image_list = os.listdir(os.path.join(path))
        for image_name in image_list:
            number_of_test_image_count += 1

    print('<----------TRAIN START ---------->')
    train_data = []
    train_labels = []

    color_list = os.listdir(TRAIN_PATH)
    with tqdm(total=number_of_train_image_count) as pbar:
        for index, color_name in enumerate(color_list):
            path = os.path.join(TRAIN_PATH, color_name)
            image_list = os.listdir(os.path.join(path))
            for image_name in image_list:
                image = read_image(os.path.join(path, image_name))

                histogram_features = normalized_color_histogram(image)
                moment_features = color_moment(image)
                cdc_features = normalize_vector(cdc(image))
                ccv_features = normalize_vector(ccv(image))
                feature = np.concatenate([histogram_features, moment_features, cdc_features, ccv_features])

                train_data.append(feature)
                train_labels.append(index)
                # pbar.update(1)
                # print(' ', color_name, image_name)

    train_data = np.nan_to_num(train_data, nan=0.0)

    normalize_moment_feature(train_data, BIN_SIZE * image.shape[2], image.shape[2])
    

    print('<----------TEST START ---------->')

    for k in [1, 5]:
        for metric_name, metric_func in distance_metrics.items():
            model = KNeighborsClassifier(n_neighbors=k, metric=metric_func)
            model.fit(train_data, train_labels)

            test_data = []
            test_labels = []
            color_list = os.listdir(TEST_PATH)

            with tqdm(total=number_of_test_image_count) as pbar:
                for index, color_name in enumerate(color_list):
                    path = os.path.join(TEST_PATH, color_name)
                    image_list = os.listdir(os.path.join(path))
                    for image_name in image_list:
                        image = read_image(os.path.join(path, image_name))

                        histogram_features = normalized_color_histogram(image)
                        moment_features = color_moment(image)
                        cdc_features = normalize_vector(cdc(image))
                        ccv_features = normalize_vector(ccv(image))
                        
                        feature = np.concatenate([histogram_features, moment_features, cdc_features, ccv_features])

                        test_data.append(feature)
                        test_labels.append(index)
                        # pbar.update(1)
                        # print(' ', color_name, image_name)

            # if np.any(np.isnan(test_data)):
            #     print("Error : NaN-2")
            #     test_data = np.nan_to_num(test_data, nan=0.0)
            #     print("Da xu li NaN-2")

            normalize_moment_feature(test_data, BIN_SIZE * image.shape[2], image.shape[2])

            prediction = model.predict(test_data)
            accuracy = metrics.accuracy_score(test_labels, prediction)
            print(f"Accuracy for k={k}, Metric={metric_name}: {accuracy}")
            print(confusion_matrix(test_labels, prediction))
