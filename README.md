# Python + OpenCV + YOLO
이 프로젝트는 Python과 OpenCV를 활용하여 YOLO(You Only Look Once) 객체 탐지 모델을 실행하는 예제.
이미지는 공공데이터 포털(https://www.data.go.kr/ )에서 제공하는 천안시 도로교통 CCTV 스트림을 활용함.


## Environment (환경)
- Python (v3.13 or higher)
- OpenCV module (opencv-python-4.12)
- YOLO module (ultralytics-8.3)


## YOLO 모델 파일
- YOLO 모델 파일(`*.pt`)은 크기때문에 git에 포함시키지 않음.
- 여러 모델을 테스트 해본 결과 현재 영상에서는 YOLO11이 가장 탐지가 잘되었음.


## 스크린샷

[![2025-08-29-11-02-43.gif](https://i.postimg.cc/ZRpC7Hd1/2025-08-29-11-02-43.gif)](https://postimg.cc/0M5krpZf)