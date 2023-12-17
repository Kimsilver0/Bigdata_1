# OpenCV를 이용한 영상 재생과 바운딩 박스 표시
# Reservation 좌석 위한 좌표 얻기

from pathlib import Path
import torch
import cv2

# 모델 로드
model_path = Path("C:/Users/grace/Downloads/yolov5/content/yolov5/runs/train/kick_results/weights/best.pt")
model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)

# 비디오 로드
video_path = r'C:\Users\grace\Videos\Captures\test14.mp4'
video = cv2.VideoCapture(video_path)

detected_objects = []

while True:
    ret, frame = video.read()

    if not ret:
        break

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

# 신뢰도가 0.5 이상인 모든 바운딩 박스의 좌표를 출력
for obj in detected_objects:
    if float(obj['label'].split(' ')[-1]) >= 0.5:
        print(f"Label: {obj['label']}, 바운딩 박스 좌표: (x1={obj['x1']}, y1={obj['y1']}), (x2={obj['x2']}, y2={obj['y2']})")

        # 처음에 잡힌 바운딩 박스의 좌표값 만을 출력