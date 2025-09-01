import cv2
from ultralytics import YOLO
import os
import argparse
from datetime import datetime

def main(output_dir):
    model = YOLO('yolo11n.pt')  # yolo11n
    rtsp_url = "http://210.99.70.120:1935/live/cctv001.stream/playlist.m3u8"
    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return
    os.makedirs(output_dir, exist_ok=True)
    last_saved_second = None
    while True:
        frame_capture_time = datetime.now()
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame from stream.")
            break
        processing_start = datetime.now()
        results = model(frame, stream=True)
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                if model.names[class_id] in ['person', 'bicycle', 'car', 'motorcycle', 'bus']:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    confidence = float(box.conf[0])
                    label = f"{model.names[class_id]} {confidence:.2f}"
                    if confidence < 0.5:
                        color = (0, 0, 255)  # Red
                    elif confidence < 0.8:
                        color = (0, 255, 255)  # Yellow
                    else:
                        color = (0, 255, 0)  # Green
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
                    
        processing_end = datetime.now()
        # Calculate and print processing time
        capture_str = f"Frame Capture: {frame_capture_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}"
        processing_str = f"Processing Time: {(processing_end - processing_start).total_seconds():.3f}s"
        text = f"{capture_str} | {processing_str}"
        text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        text_x = 10
        text_y = frame.shape[0] - 10
        cv2.rectangle(frame, (0, frame.shape[0] - text_size[1] - 20), (frame.shape[1], frame.shape[0]), (0,0,0), -1)
        cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

        # Save one image per second, keep only 60 images
        now = datetime.now()
        current_second = now.strftime('%Y%m%d_%H%M%S')
        if last_saved_second != current_second:
            out_path = os.path.join(output_dir, f"frame_{current_second}.jpg")
            cv2.imwrite(out_path, frame)
            last_saved_second = current_second
            # Remove old images if more than 60 exist
            jpgs = sorted([f for f in os.listdir(output_dir) if f.endswith('.jpg')])
            if len(jpgs) > 60:
                for old_file in jpgs[:-60]:
                    try:
                        os.remove(os.path.join(output_dir, old_file))
                    except Exception:
                        pass
        # Optionally, add a small sleep to reduce disk I/O
        # time.sleep(0.05)
    cap.release()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CCTV Object Detection and Save Frames")
    parser.add_argument('--output_dir', type=str, required=True, help='Directory to save output frames')
    args = parser.parse_args()
    main(args.output_dir)
