import cv2
import face_recognition
import pickle
import time
import numpy as np
import database.redis_cli as redis


def detect_moire_pattern(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    dft = cv2.dft(np.float32(gray), flags=cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)
    magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]) + 1)
    mean_freq_intensity = np.mean(magnitude_spectrum)
    return mean_freq_intensity > 150


def detect_blur(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return laplacian_var < 50


def face_handling(frame):
    if detect_moire_pattern(frame):
        print('Detected moiré pattern. Possible screen photo.')
        return None
    if detect_blur(frame):
        print('Image too blurry. Possible screen photo.')
        return None

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_encodings = face_recognition.face_encodings(rgb_frame)

    if len(face_encodings) == 0:
        print('No face detected\n')
        return None

    return pickle.dumps(face_encodings[0])


def face_compare(frame):
    start_time = time.time()
    error_reason = None

    if detect_moire_pattern(frame):
        error_reason = 'Possible screen photo detected'
        elapsed_time = time.time() - start_time
        return None, None, elapsed_time, error_reason
    if detect_blur(frame):
        error_reason = 'Image too blurry'
        elapsed_time = time.time() - start_time
        return None, None, elapsed_time, error_reason

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_encodings = face_recognition.face_encodings(rgb_frame)

    if not face_encodings:
        error_reason = 'No face detected'
        elapsed_time = time.time() - start_time
        return None, None, elapsed_time, error_reason

    known_users = redis.get_info()
    best_match = None
    best_confidence = 0.0

    for username, encodings in known_users:
        known_encoding = pickle.loads(encodings)
        distance = face_recognition.face_distance([known_encoding], face_encodings[0])[0]
        confidence = (0.6 - distance) / (0.6 - 0.3)
        confidence = max(0.0, min(1.0, confidence))

        if confidence > best_confidence:
            best_match = username
            best_confidence = confidence

    elapsed_time = time.time() - start_time

    if best_match:
        return best_match, best_confidence, elapsed_time, None
    else:
        error_reason = 'Face not recognized'
        return None, None, elapsed_time, error_reason
