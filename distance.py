from pathlib import Path
import torch
import numpy as np
import cv2
import math

# 모델 로드
model_path = Path("C:/Users/grace/Downloads/yolov5/content/yolov5/runs/train/kick_results/weights/best.pt")
model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)

# 비디오 로드
video_path = r'C:\Users\grace\Videos\Captures\test21.mp4'
video = cv2.VideoCapture(video_path)

detected_objects = []

while True:
    ret, frame = video.read()

    if not ret:
        break

    # 프레임을 원본 크기로 변경
    frame = cv2.resize(frame, (frame.shape[1], frame.shape[0]), interpolation=cv2.INTER_LINEAR)

    results = model(frame)  # YOLOv5 모델로 객체 감지

    for result in results.pred:
        for *xyxy, conf, cls in result:
            # 각 객체에 대한 정보 추출
            x1, y1, x2, y2 = map(int, xyxy)
            label = f'{model.names[int(cls)]} {conf:.2f}'

            # 바운딩 박스 및 클래스 레이블을 영상에 표시
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(frame, label, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            # 바운딩 박스의 좌표를 리스트에 추가
            detected_objects.append({'label': label, 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2})

    cv2.imshow('Video', frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):  # 'q' 키를 눌러 종료
        break

video.release()
cv2.destroyAllWindows()

# guide_blocks와 kick_board 바운딩 박스 정보
guide_blocks_coords = {'x1': 685, 'y1': 780, 'x2': 901, 'y2': 1039}
kick_board_coords = {'x1': 810, 'y1': 83, 'x2': 1254, 'y2': 635}

# 중심점 계산
guide_blocks_center = ((guide_blocks_coords['x1'] + guide_blocks_coords['x2']) / 2,
                       (guide_blocks_coords['y1'] + guide_blocks_coords['y2']) / 2)
kick_board_center = ((kick_board_coords['x1'] + kick_board_coords['x2']) / 2,
                     (kick_board_coords['y1'] + kick_board_coords['y2']) / 2)

# 두 중심점을 연결하는 선을 그릴 새로운 이미지 생성
line_image = np.zeros((1080, 1920, 3), dtype=np.uint8)  # 가정한 동영상 크기

# 중심점을 이용하여 선 그리기
cv2.line(line_image, (int(guide_blocks_center[0]), int(guide_blocks_center[1])),
         (int(kick_board_center[0]), int(kick_board_center[1])), (0, 0, 255), 2)

# 중심점 좌표 출력
cv2.putText(line_image, f"Guide Blocks: ({guide_blocks_center[0]}, {guide_blocks_center[1]})",
            (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(line_image, f"Kick Board: ({kick_board_center[0]}, {kick_board_center[1]})",
            (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

# 선을 그린 이미지 출력
cv2.imshow('Line Image', line_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 두 중심점 간의 거리 계산
distance = math.sqrt((kick_board_center[0] - guide_blocks_center[0])**2 + 
                     (kick_board_center[1] - guide_blocks_center[1])**2)

# 두 중심점과 거리 출력
print(f"두 중심점 간의 거리: {distance:.2f}")
if distance <= 1000:
    print("점자 블록 위에서 킥보드를 수거해주십시오. 불법주차입니다.")
else:
    print("올바른 주차입니다.")