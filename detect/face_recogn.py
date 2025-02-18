import cv2
import face_recognition
import pickle
import database.db as db

def face_handling(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_encodings = face_recognition.face_encodings(rgb_frame)

    if len(face_encodings) == 0:
        print('No face detected\n')
        return None

    return pickle.dumps(face_encodings[0])


def face_compare(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_encodings = face_recognition.face_encodings(rgb_frame)
    if not face_encodings:
        return None
    known_users = db.get_info()

    for username, encodings in known_users:
        known_encoding = pickle.loads(encodings)
        match = face_recognition.compare_faces([known_encoding], face_encodings[0])
        if match[0]:
            return username
    return None