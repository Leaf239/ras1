import cv2
import time
import numpy as np
import urllib

# 자동차 탐지에 사용할 Haarcascade XML 파일 경로
car_cascade_path = 'haarcascade_car.xml'

# 자동차 탐지기 생성
car_cascade = cv2.CascadeClassifier(car_cascade_path)

if car_cascade.empty():
    url = 'https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/cars.xml'
    urllib.request.urlretrieve(url, 'cars.xml')
    car_cascade.load('cars.xml')

# 카메라 열기
cap_right = cv2.VideoCapture(1, cv2.CAP_DSHOW)                    
cap_left =  cv2.VideoCapture(2, cv2.CAP_DSHOW)


# 이전 프레임의 시간을 저장할 변수
prev_time = None

def calculate_depth(disparity, f, B):
    depth = f * B / (disparity + 0.0001)  # Add small value to avoid division by zero
    return depth

def pixel_to_cm(disparity, B, f):

    disparity_cm = f * B / disparity
    return disparity_cm


# 스테레오 비전 설정
B = 5              # 카메라 사이 거리 [cm]
f = 8               # 카메라 렌즈의 초점 거리 [mm]
alpha = 60       # 카메라 수평면의 시야각 [degrees]

prev_depth = None
prev_time = time.time()

def calculate_speed(depth):
    global prev_depth, prev_time
    current_time = time.time()
    if prev_depth is not None:
        # Calculate time difference
        time_difference = current_time - prev_time
        # Calculate speed using depth difference and time difference
        speed = abs(depth - prev_depth) / time_difference
        return speed
    else:
        return 0


while True:
    start_time = time.time()

    ret_left, frame_left = cap_left.read()
    ret_right, frame_right = cap_right.read()

    if not ret_left or not ret_right:
        break


    gray_left = cv2.cvtColor(frame_left, cv2.COLOR_BGR2GRAY)
    gray_right = cv2.cvtColor(frame_right, cv2.COLOR_BGR2GRAY)

    cars_left = car_cascade.detectMultiScale(gray_left, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    cars_right = car_cascade.detectMultiScale(gray_right, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around the detected cars and find their centroids in both frames
    car_centroids_left = []
    for (x, y, w, h) in cars_left:
        cv2.rectangle(frame_left, (x, y), (x+w, y+h), (0, 255, 0), 2)
        car_centroids_left.append((x + w // 2, y + h // 2))

    car_centroids_right = []
    for (x, y, w, h) in cars_right:
        cv2.rectangle(frame_right, (x, y), (x+w, y+h), (0, 255, 0), 2)
        car_centroids_right.append((x + w // 2, y + h // 2))

    # Match detected cars between left and right frames
    for centroid_left in car_centroids_left:
        min_disparity = float('inf')
        best_match = None

        for centroid_right in car_centroids_right:
            disparity = centroid_right[0] - centroid_left[0]
            if disparity < min_disparity:
                min_disparity = disparity
                best_match = centroid_right

        if best_match is not None:
            depth = calculate_depth(min_disparity, f, B)
            print("Depth:", round(depth, 2), "cm")

        if best_match is not None:
            print("Disparity:", min_disparity)

    speed = calculate_speed(depth)
    print("Speed:", round(speed, 2), "cm/s")

    # Calculate and display FPS
    end_time = time.time()
    fps = 1 / (end_time - start_time)
    print("FPS:", round(fps, 2))

    
    # Display frames
    cv2.imshow("Left Frame", frame_left)
    cv2.imshow("Right Frame", frame_right)

    # Check for exit key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release capture objects and destroy windows
cap_left.release()
cap_right.release()
cv2.destroyAllWindows()

