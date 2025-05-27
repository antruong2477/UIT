import cv2

print("OpenCV version:", cv2.__version__)
cap = cv2.VideoCapture(0)
if cap.isOpened():
    print("Camera is working.")
else:
    print("Cannot access camera.")
cap.release()
