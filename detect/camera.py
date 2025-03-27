import cv2
import face_recognition
import time
import requests
import numpy as np
import imutils
from config.local import camera_url


def video_capture():
    url = camera_url
    start_time = None
    print("Please don't move\n")

    while True:
        try:
            img_resp = requests.get(url, timeout=5)
            img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
            frame = cv2.imdecode(img_arr, -1)

            if frame is None:
                continue
        except Exception as e:
            print(f'Error getting frame: {e}')
            return None

        frame = imutils.resize(frame, width=1000)

        cv2.imshow('Face Recognition - Press Q to exit', frame)

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)

        if face_locations:
            if start_time is None:
                start_time = time.time()
                print('Face detected! Keep steady...')
            elif time.time() - start_time >= 2:
                print('Analyzing your face...')
                cv2.destroyAllWindows()
                return frame
        else:
            start_time = None

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    return None
