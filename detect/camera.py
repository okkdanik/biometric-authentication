import cv2
import face_recognition
import time

def video_capture():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("We couldn't open your camera")
        return None

    print("Please don't move\n")
    start_time = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow('Face Recognition - Press Q to exit', frame)

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)

        if face_locations:
            if start_time is None:
                start_time = time.time()

            if time.time() - start_time >= 2:
                print('Analyzing your face...')
                cap.release()
                cv2.destroyAllWindows()
                return frame
        else:
            start_time = None

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None
