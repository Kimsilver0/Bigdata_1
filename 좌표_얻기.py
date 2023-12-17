from pathlib import Path
import torch
import cv2
import math

# 모델 로드
model_path = Path("C:/Users/grace/Downloads/yolov5/content/yolov5/runs/train/kick_results/weights/best.pt")
model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)

# 이미지 로드
image_path = r'C:\Users\grace\Downloads\test_results\content\yolov5\runs\detect\exp12\19.jpeg'
image = cv2.imread(image_path)

detected_objects = []

# 이미지에 대해 객체 감지 수행
results = model(image)  # YOLOv5 모델로 객체 감지

# 신뢰도가 0.6 이상인 바운딩 박스의 중심점 계산
kick_board_coords = None
guide_block_coords = None
other_boxes = []

for result in results.pred:
    for *xyxy, conf, cls in result:
        label = model.names[int(cls)]
        if conf >= 0.6:
            x1, y1, x2, y2 = map(int, xyxy)
            x_center, y_center = (x1 + x2) / 2, (y1 + y2) / 2

            if label == 'kick_board':
                kick_board_coords = (x_center, y_center)
            elif label == 'guide_block':
                guide_block_coords = (x_center, y_center)
            else:
                other_boxes.append((x_center, y_center))

# 킥보드와 가이드 블록 중심점 사이의 거리 계산
if kick_board_coords and guide_block_coords:
    distance = math.sqrt((kick_board_coords[0] - guide_block_coords[0])**2 + (kick_board_coords[1] - guide_block_coords[1])**2)
    for box in other_boxes:
        dist_to_kick = math.sqrt((kick_board_coords[0] - box[0])**2 + (kick_board_coords[1] - box[1])**2)
        dist_to_guide = math.sqrt((guide_block_coords[0] - box[0])**2 + (guide_block_coords[1] - box[1])**2)
        if dist_to_kick + dist_to_guide > distance:
            print("킥보드가 불법주차 되어 있습니다.")
            break
    else:
        print("킥보드가 올바르게 주차되어 있습니다.")
else:
    print("킥보드 또는 가이드 블록이 감지되지 않았습니다.")
