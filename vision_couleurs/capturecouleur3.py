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
        # indiquant la présence de la couleur dans la partie de l'image.
        if np.sum(mask) > 0:  # Vérification sommaire de la présence de la couleur
            detected_colors[color] = True
        else:
            detected_colors[color] = False

    return detected_colors

def capture_and_detect():
    cap = cv2.VideoCapture(0)
    
    # Capture d'une seule image
    ret, frame = cap.read()
    if not ret:
        print("Erreur lors de la capture de l'image")
        return
    cap.release()

    # Diviser l'image en trois parties égales (gauche, centre, droite)
    height, width, _ = frame.shape
    third_width = width // 3

    # ROI pour chaque partie de l'image
    roi_left = (0, 0, third_width, height)
    roi_center = (third_width, 0, third_width, height)
    roi_right = (2 * third_width, 0, third_width, height)

    # Détecter les couleurs dans chaque partie de l'image
    detected_colors_left = detect_colors(frame[:, :third_width])
    detected_colors_center = detect_colors(frame[:, third_width:2*third_width])
    detected_colors_right = detect_colors(frame[:, 2*third_width:])

    # Mettre à jour les résultats pour inclure False si la couleur n'a pas été détectée
    for color in COLOR_RANGES.keys():
        if color not in detected_colors_left:
            detected_colors_left[color] = False
        if color not in detected_colors_center:
            detected_colors_center[color] = False
        if color not in detected_colors_right:
            detected_colors_right[color] = False

    print("Couleurs détectées à gauche : ", detected_colors_left)
    print("Couleurs détectées au centre : ", detected_colors_center)
    print("Couleurs détectées à droite : ", detected_colors_right)

    # Afficher l'image capturée avec des zones où les couleurs ont été détectées
    cv2.imshow('Captured Image', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_and_detect()
