import cv2
import numpy as np

COLOR_RANGES = {
    "rouge": ((0, 150, 50), (10, 255, 255)),
    "vert": ((40, 70, 60), (80, 255, 255)),
    "bleu": ((100, 150, 0), (140, 255, 255)),
    "jaune": ((25, 70, 120), (30, 255, 255)),
}

def detect_colors_in_pillar(hsv_frame, pillar_bounds):
    detected_colors = {}
    pillar_frame = hsv_frame[:, pillar_bounds[0]:pillar_bounds[1]]

    for color, (lower, upper) in COLOR_RANGES.items():
        lower_bound = np.array(lower)
        upper_bound = np.array(upper)
        mask = cv2.inRange(pillar_frame, lower_bound, upper_bound)
        result = cv2.bitwise_and(pillar_frame, pillar_frame, mask=mask)

        if np.sum(mask) > 0:  # Simple check for presence of the color
            detected_colors[color] = True

    return detected_colors

def capture_and_detect():
    cap = cv2.VideoCapture(0)
    
    ret, frame = cap.read()
    if not ret:
        print("Error capturing image")
        return
    cap.release()

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    width = frame.shape[1]
    third_width = width // 3

    left_pillar = detect_colors_in_pillar(hsv_frame, (0, third_width))
    center_pillar = detect_colors_in_pillar(hsv_frame, (third_width, 2 * third_width))
    right_pillar = detect_colors_in_pillar(hsv_frame, (2 * third_width, width))

    print("Colors in left pillar: ", left_pillar)
    print("Colors in center pillar: ", center_pillar)
    print("Colors in right pillar: ", right_pillar)

    cv2.imshow('Captured Image', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_and_detect()
