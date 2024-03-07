import cv2
import numpy as np

# Plages de couleurs HSV pour la détection
COLOR_RANGES = {
    "rouge": ((0, 150, 50), (10, 255, 255)),  # Rouge
    "vert": ((40, 70, 60), (80, 255, 255)),  # Vert
    "bleu": ((100, 150, 0), (140, 255, 255)),  # Bleu
    "jaune": ((25, 70, 120), (30, 255, 255)),  # Jaune
}

def detect_colors(image):
    hsv_frame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    detected_colors = {}

    for color, (lower, upper) in COLOR_RANGES.items():
        lower_bound = np.array(lower)
        upper_bound = np.array(upper)
        mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)
        result = cv2.bitwise_and(image, image, mask=mask)
        
        # Vous pouvez ici ajouter une logique pour vérifier si le résultat n'est pas vide, 
        # indiquant la présence de la couleur dans l'image.
        if np.sum(mask) > 0:  # Vérification sommaire de la présence de la couleur
            detected_colors[color] = True

    return detected_colors

def capture_and_detect():
    cap = cv2.VideoCapture(0)
    
    # Capture d'une seule image
    ret, frame = cap.read()
    if not ret:
        print("Erreur lors de la capture de l'image")
        return
    cap.release()

    # Appel de la fonction de détection
    detected_colors = detect_colors(frame)

    print("Couleurs détectées : ", detected_colors)

    # Afficher l'image capturée avec des zones où les couleurs ont été détectées
    cv2.imshow('Captured Image', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_and_detect()
