import cv2
import numpy as np

def detect_colors(image, hsv_values):
    # Décomposition des valeurs HSV
    low_h, high_h, low_s, high_s, low_v, high_v = hsv_values

    # Convertir l'image de l'espace couleur BGR à HSV
    hsv_frame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Définir les plages de couleur pour la détection
    lower_bound = np.array([low_h, low_s, low_v])
    upper_bound = np.array([high_h, high_s, high_v])

    # Créer le masque pour isoler la couleur dans l'image
    mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)

    # Appliquer le masque à l'image originale pour obtenir la couleur détectée
    result = cv2.bitwise_and(image, image, mask=mask)

    return result

def on_trackbar_change(_):
    # Récupérer l'image sauvegardée
    frame = cv2.imread('captured_frame.jpg')

    # Lire les valeurs actuelles des trackbars
    low_h = cv2.getTrackbarPos('Low H', 'Trackbars')
    high_h = cv2.getTrackbarPos('High H', 'Trackbars')
    low_s = cv2.getTrackbarPos('Low S', 'Trackbars')
    high_s = cv2.getTrackbarPos('High S', 'Trackbars')
    low_v = cv2.getTrackbarPos('Low V', 'Trackbars')
    high_v = cv2.getTrackbarPos('High V', 'Trackbars')

    hsv_values = (low_h, high_h, low_s, high_s, low_v, high_v)
    result = detect_colors(frame, hsv_values)

    # Afficher le résultat
    cv2.imshow('Detected Colors', result)

def main():
    # Initialisation de la capture vidéo
    cap = cv2.VideoCapture(0)
    
    # Capture d'une seule image
    ret, frame = cap.read()
    if ret:
        cv2.imwrite('captured_frame.jpg', frame)
    else:
        print("Erreur lors de la capture de l'image")
        return
    cap.release()

    # Création d'une fenêtre pour les curseurs
    cv2.namedWindow('Trackbars')

    # Création des curseurs pour régler les valeurs HSV
    cv2.createTrackbar('Low H', 'Trackbars', 0, 180, on_trackbar_change)
    cv2.createTrackbar('High H', 'Trackbars', 180, 180, on_trackbar_change)
    cv2.createTrackbar('Low S', 'Trackbars', 0, 255, on_trackbar_change)
    cv2.createTrackbar('High S', 'Trackbars', 255, 255, on_trackbar_change)
    cv2.createTrackbar('Low V', 'Trackbars', 0, 255, on_trackbar_change)
    cv2.createTrackbar('High V', 'Trackbars', 255, 255, on_trackbar_change)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Aucune image capturée")
            break

        # Lecture des valeurs des curseurs
        low_h = cv2.getTrackbarPos('Low H', 'Trackbars')
        high_h = cv2.getTrackbarPos('High H', 'Trackbars')
        low_s = cv2.getTrackbarPos('Low S', 'Trackbars')
        high_s = cv2.getTrackbarPos('High S', 'Trackbars')
        low_v = cv2.getTrackbarPos('Low V', 'Trackbars')
        high_v = cv2.getTrackbarPos('High V', 'Trackbars')

        hsv_values = (low_h, high_h, low_s, high_s, low_v, high_v)
        result = detect_colors(frame, hsv_values)

        # Affichage du résultat
        cv2.imshow('Detected Colors', result)

        # Attendre la touche 'q' pour quitter
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Attendre indéfiniment jusqu'à ce qu'une touche soit pressée
    cv2.waitKey(0)

    # Nettoyage
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
