import cv2
import numpy as np
from gtts import gTTS
import os

# Plages de couleurs HSV pour la détection
COLOR_RANGES = {
    "rouge": ((0, 120, 70), (10, 255, 255)),
    "vert": ((40, 40, 40), (70, 255, 255)),
    "bleu": ((100, 150, 20), (140, 255, 255)),
    "jaune": ((15, 100, 100), (70, 255, 255)),
}

def detect_colors(image):
    hsv_frame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    detected_colors = {}

    for color, (lower, upper) in COLOR_RANGES.items():
        lower_bound = np.array(lower)
        upper_bound = np.array(upper)
        mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)
        
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        color_pixels = np.sum(mask)
        total_pixels = image.shape[0] * image.shape[1]
        if color_pixels / total_pixels > 0.01:
            detected_colors[color] = True
        else:
            detected_colors[color] = False

    return detected_colors

def speak_message(message):
    tts = gTTS(message, lang='fr')
    tts.save('message.mp3')
    os.system('mpg321 message.mp3')

def capture_and_detect():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if not ret:
        print("Erreur lors de la capture de l'image")
        return
    cap.release()

    height, width, _ = frame.shape
    third_width = width // 3

    detected_colors_left = detect_colors(frame[:, :third_width])
    detected_colors_center = detect_colors(frame[:, third_width:2*third_width])
    detected_colors_right = detect_colors(frame[:, 2*third_width:])

    for color in COLOR_RANGES.keys():
        if color not in detected_colors_left:
            detected_colors_left[color] = False
        if color not in detected_colors_center:
            detected_colors_center[color] = False
        if color not in detected_colors_right:
            detected_colors_right[color] = False

    # Vérifier si toutes les couleurs sont à gauche
    if all(detected_colors_left.values()) and not any(detected_colors_center.values()) and not any(detected_colors_right.values()):
        message = "Toutes les pièces ont bien été placées à gauche. La partie peut commencer."
    else:
        message = "Le jeu ne peut pas commencer car les pièces n'ont pas été correctement positionnées. Veuillez placer les pièces correctement s'il vous plait"

    print(message)
    speak_message(message)

    cv2.imshow('Captured Image', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_and_detect()
