import cv2
import face_recognition
import pickle
import time
import database.redis_cli as redis


def face_handling(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_encodings = face_recognition.face_encodings(rgb_frame)

    if len(face_encodings) == 0:
        print('No face detected\n')
        return None

    return pickle.dumps(face_encodings[0])


def face_compare(frame):
    start_time = time.time()

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_encodings = face_recognition.face_encodings(rgb_frame)

    if not face_encodings:
        return None, None, None

    known_users = redis.get_info()
    best_match = None
    best_confidence = 0.0

    for username, encodings in known_users:
        known_encoding = pickle.loads(encodings)
        distance = face_recognition.face_distance([known_encoding], face_encodings[0])[0]

        confidence = max(0.0, 1 - ((distance - 0.3) / (0.6 - 0.3)))

        if confidence > best_confidence:
            best_match = username
            best_confidence = confidence

    elapsed_time = time.time() - start_time

    if best_match:
        return best_match, best_confidence, elapsed_time
    return None, None, elapsed_time
