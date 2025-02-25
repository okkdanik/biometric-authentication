import cv2

def video_capture():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("We couldn't open your camera")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow('REC...', frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            cap.release()
            cv2.destroyAllWindows()
            return frame
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return None
