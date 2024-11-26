import cv2
import mss
import numpy
import winsound

def load_templates():
    templates = {
        "STOP sign": cv2.imread('img/road-signs/stop_sign.png', cv2.IMREAD_GRAYSCALE),
        "Turn left sign": cv2.imread('img/road-signs/turn_left_sign.png', cv2.IMREAD_GRAYSCALE),
        "Turn right sign": cv2.imread('img/road-signs/turn_right_sign.png', cv2.IMREAD_GRAYSCALE),
        "Turn right sign small": cv2.imread('img/road-signs/turn_right_small.png', cv2.IMREAD_GRAYSCALE)
    }

    for name, template in templates.items():
        if template is None:
            print(f"Error: Template image '{name}' not found!")
            exit(1)

    return templates

def detect_road_signs():
    templates = load_templates()

    match_threshold = 0.8

    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Full screen capture (monitor[1] is the main screen)

        while True:
            screenshot = sct.grab(monitor)
            screen_image = numpy.array(screenshot)
            screen_gray = cv2.cvtColor(screen_image, cv2.COLOR_BGR2GRAY)

            for name, template in templates.items():
                result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
                locations = numpy.nonzero(result >= match_threshold)

                if len(locations[0]) > 0:
                    print(f"{name} detected!")

def detect_qr_code():
    print(f"not ready yet")
# def capture_screen_and_detect_qr():
#     qr_codes = set()
#
#     # Capture screen
#     with mss.mss() as sct:
#         monitor = sct.monitors[1]
#         qr_detector = cv2.QRCodeDetector()
#
#         while True:
#             screenshot = sct.grab(monitor)
#
#             img = numpy.array(screenshot) # Convert to numpy array
#             img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Convert to grayscale
#
#             qr_code, points, _ = qr_detector.detectAndDecode(img) # Detect and decode QR code
#
#             if points is not None and qr_code and qr_code not in qr_codes:
#                 qr_codes.add(qr_code)
#                 print(f"New QR code detected: {qr_codes}")
#                 winsound.PlaySound("rooster.wav", winsound.SND_FILENAME)

def main():
    detect_road_signs()
    detect_qr_code()

if __name__ == "__main__":
    main()
