import cv2
import numpy as np

# Plages de couleurs HSV pour la détection
COLOR_RANGES = {
    "rouge": ((0, 150, 50), (10, 255, 255)),
    "vert": ((40, 70, 60), (80, 255, 255)),
    "bleu": ((100, 150, 0), (140, 255, 255)),
    "jaune": ((25, 70, 120), (30, 255, 255)),
}

SIZE_MAPPING = {
    "rouge": 4,  # La plus grande pièce
    "vert": 3,
    "bleu": 2,
    "jaune": 1,  # La plus petite pièce
}

# Cette fonction est un exemple de détection de contours pour une couleur spécifique.
def detect_and_label_disks(image, lower_color, upper_color, color_name):
    # Conversion de l'image en espace de couleur HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Application du masque de couleur
    mask = cv2.inRange(hsv, lower_color, upper_color)
    # Détection des contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    labeled_disks = []
    for cnt in contours:
        # Filtrage selon la taille des contours trouvés
        area = cv2.contourArea(cnt)
        if area > 100:  # La taille minimale pour être considéré comme un disque
            labeled_disks.append((SIZE_MAPPING[color_name], cnt))
    return labeled_disks

# Fonction pour analyser un pilier et renvoyer l'état des pièces dans l'ordre décroissant.
def analyze_pillar(image):
    all_disks = []
    for color_name, (lower, upper) in COLOR_RANGES.items():
        all_disks.extend(detect_and_label_disks(image, np.array(lower), np.array(upper), color_name))
    # Trier les disques par taille
    all_disks.sort(reverse=True, key=lambda x: x[0])
    return [size for size, cnt in all_disks]

# Fonction pour obtenir l'état actuel du jeu
def get_current_game_state(image_path):
    image = cv2.imread(image_path)
    # Découpage de l'image en trois parties égales pour chaque pilier
    height, width = image.shape[:2]
    third_width = width // 3
    piliers = [image[:, i * third_width:(i + 1) * third_width] for i in range(3)]
    # Analyser chaque pilier
    game_state = [analyze_pillar(pilier_image) for pilier_image in piliers]
    return game_state

# Image de test (remplacer par le chemin de mon image réelle)
image_path = '/Users/abderrahmanebenali/Downloads/IMG_9674.png'  
game_state = get_current_game_state(image_path)

# Afficher l'état du jeu
for i, state in enumerate(game_state, 1):
    print(f"Pilier {i}: {state}")
