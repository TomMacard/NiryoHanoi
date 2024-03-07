import cv2
import numpy as np

# Capture vidéo à partir de la webcam intégrée
cap = cv2.VideoCapture(0)  # L'argument 0 indique la première webcam disponible

while True:
    ret, frame = cap.read()  # Lecture d'une frame de la webcam

    if not ret:
        break

    # Convertir l'image de la webcam de l'espace couleur BGR à HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Définir les plages de couleur pour la détection
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])

    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])

    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    lower_blue = np.array([100, 100, 100])
    upper_blue = np.array([140, 255, 255])

    # Créer les masques pour isoler les couleurs dans l'image
    mask_yellow = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)
    mask_green = cv2.inRange(hsv_frame, lower_green, upper_green)
    mask_red = cv2.inRange(hsv_frame, lower_red, upper_red)
    mask_blue = cv2.inRange(hsv_frame, lower_blue, upper_blue)

    # Trouver les contours dans les images masquées
    contours_yellow, _ = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Dessiner des cercles englobants autour des contours détectés pour chaque couleur
    for cnt in contours_yellow:
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        center = (int(x), int(y))
        radius = int(radius)
        cv2.circle(frame, center, radius, (0, 255, 255), 2)

    for cnt in contours_green:
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        center = (int(x), int(y))
        radius = int(radius)
        cv2.circle(frame, center, radius, (0, 255, 0), 2)

    for cnt in contours_red:
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        center = (int(x), int(y))
        radius = int(radius)
        cv2.circle(frame, center, radius, (0, 0, 255), 2)

    for cnt in contours_blue:
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        center = (int(x), int(y))
        radius = int(radius)
        cv2.circle(frame, center, radius, (255, 0, 0), 2)

    # Afficher la vidéo avec les cercles englobants des contours de chaque couleur
    cv2.imshow('Contours', frame)

    # Attendre la pression de la touche 'q' pour quitter la boucle
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# Libérer la capture et fermer les fenêtres
cap.release()
cv2.destroyAllWindows()
