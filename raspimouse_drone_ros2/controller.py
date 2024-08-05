#!/home/nakahira/work/yolov8/bin/python
import cv2
import numpy as np
from ultralytics import YOLO
import rclpy
import drone
#!/usr/bin/env python3
def main(args=None):
    # ウェブカメラのキャプチャを開始
    video_path = 2
    cap = cv2.VideoCapture(video_path)
    img_size = np.array([cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)])
    # Load a pretrained YOLOv8n model
    model_path = "/home/nakahira/ros2_ws/src/raspimouse_drone_ros2/pinpon.pt"
   # model_path = '/home/nakahira/work/yolov8n.pt'
    model = YOLO(model_path)

    rclpy.init()
    drone_obj = drone.DroneControl(img_size)
    rate = drone_obj.create_rate(10)
    # キャプチャがオープンしている間続ける
    while(cap.isOpened() and rclpy.ok()):
        # フレームを読み込む
        ret, frame = cap.read()
        if ret == True:
            # フレームを表示
            detections = model(frame)
            detection = detections[0]
            drone_obj.getDronePoint(detection)
            drone_obj.getMovingDerection()
            frame = detection.plot()
            frame = drone_obj.OverImage(frame)
            drone_obj.sendCommand()
            cv2.imshow('Webcam Live', frame)
            rclpy.spin_once(drone_obj)
            # 'q'キーが押されたらループから抜ける
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
                break

    # キャプチャをリリースし、ウィンドウを閉じる
    cap.release()
    cv2.destroyAllWindows()
    # ros node破棄
    rclpy.shutdown()

if __name__ == '__main__':
    main()