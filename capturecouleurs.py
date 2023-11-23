import cv2
import numpy as np

def detect_colors(image):
    # Convertir l'image de l'espace couleur BGR à HSV
    hsv_frame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

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

    # Appliquer les masques aux frames originales pour obtenir les couleurs détectées
    result_yellow = cv2.bitwise_and(image, image, mask=mask_yellow)
    result_green = cv2.bitwise_and(image, image, mask=mask_green)
    result_red = cv2.bitwise_and(image, image, mask=mask_red)
    result_blue = cv2.bitwise_and(image, image, mask=mask_blue)

    # Fusionner les résultats dans une seule image
    combined_result = cv2.add(result_yellow, result_green)
    combined_result = cv2.add(combined_result, result_red)
    combined_result = cv2.add(combined_result, result_blue)

    # Afficher les résultats de la détection de couleur dans une seule fenêtre
    cv2.imshow('Combined Results', combined_result)
    cv2.waitKey(0)  # Attendre indéfiniment jusqu'à ce qu'une touche soit pressée
    cv2.destroyAllWindows()

def main():
    # Capture vidéo à partir de la webcam intégrée
    cap = cv2.VideoCapture(0)  # L'argument 0 indique la première webcam disponible

    ret, frame = cap.read()  # Lecture d'une frame de la webcam

    if not ret:
        print("Aucune image capturée")
        return

    detect_colors(frame)

    # Libérer la capture
    cap.release()

if __name__ == "__main__":
    main()