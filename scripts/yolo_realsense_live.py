import time
import cv2
import numpy as np
import pyrealsense2 as rs
from ultralytics import YOLO

WIN = "RealSense YOLOv8"

def main():
    model = YOLO("model/yolov8n.pt")

    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    pipeline.start(config)

    cv2.namedWindow(WIN, cv2.WINDOW_NORMAL)

    fullscreen = False
    t0 = time.time()
    frames_count = 0
    fps = 0.0

    print("Press 'f' to toggle fullscreen. Press 'q' to quit.")

    try:
        while True:
            frames = pipeline.wait_for_frames()
            color = frames.get_color_frame()
            if not color:
                continue

            frame = np.asanyarray(color.get_data())
            result = model(frame, verbose=False)[0]
            annotated = result.plot()

            frames_count += 1
            dt = time.time() - t0
            if dt >= 1.0:
                fps = frames_count / dt
                frames_count = 0
                t0 = time.time()

            cv2.putText(annotated, f"FPS: {fps:.1f}  (f=fullscreen, q=quit)", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            cv2.imshow(WIN, annotated)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            if key == ord("f"):
                fullscreen = not fullscreen
                cv2.setWindowProperty(
                    WIN,
                    cv2.WND_PROP_FULLSCREEN,
                    cv2.WINDOW_FULLSCREEN if fullscreen else cv2.WINDOW_NORMAL
                )
    finally:
        pipeline.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
