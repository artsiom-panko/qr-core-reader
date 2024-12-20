import cv2
import mss
import numpy
import winsound


def load_templates(template_paths):
    """
    Load template images from specified paths and return a dictionary.
    Raise an error if any template fails to load.
    """
    templates = {}
    for name, path in template_paths.items():
        template = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            raise FileNotFoundError(f"Error: Template image '{name}' not found at '{path}'!")
        templates[name] = template
    return templates


def detect_road_signs(screen_gray, templates, match_threshold=0.8):
    """
    Detect road signs on the grayscale screen image using template matching.
    Prints the name of detected signs.
    """
    for name, template in templates.items():
        result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
        if numpy.any(result >= match_threshold):
            print(f"{name} detected!")


def detect_qr_code(screen_gray, qr_detector, detected_qr_codes):
    """
    Detect QR codes on the grayscale screen image.
    Plays a sound and logs new QR codes.
    """
    qr_code, points, _ = qr_detector.detectAndDecode(screen_gray)
    if points is not None and qr_code and qr_code not in detected_qr_codes:
        detected_qr_codes.add(qr_code)
        print(f"New QR code detected: {qr_code}")
        winsound.PlaySound("rooster.wav", winsound.SND_FILENAME)


def main():
    # Define the templates and their file paths
    template_paths = {        "STOP sign": 'img/road-signs/stop_sign.png',
        "Turn left sign": 'img/road-signs/turn_left_sign.png',
        "Turn right sign": 'img/road-signs/turn_right_sign.png',
        "Turn right sign small": 'img/road-signs/turn_right_small.png',
        "Turn right sign1": 'img/road-signs/Screenshot_20241127_225248.jpg',
        "Turn right sign2": 'img/road-signs/Screenshot_20241127_225254.jpg',
        "Turn right sign3": 'img/road-signs/Screenshot_20241127_225304.jpg',
        "Turn right sign4": 'img/road-signs/Screenshot_20241127_225310.jpg',
        "Turn right sign5": 'img/road-signs/Screenshot_20241127_225357.jpg',
        "Turn right sign6": 'img/road-signs/Screenshot_20241127_225402.jpg',
        "Turn right sign7": 'img/road-signs/Screenshot_20241127_225409.jpg',
        "Turn left sign1":'img/road-signs/screenshots/Screenshot_20241128_095700.jpg',
        "Turn left sign2":'img/road-signs/screenshots/Screenshot_20241128_095708.jpg',
        "Turn left sign3":'img/road-signs/screenshots/Screenshot_20241128_095711.jpg',
        "Turn left sign4":'img/road-signs/screenshots/Screenshot_20241128_095717.jpg',
        "Turn left sign5":'img/road-signs/screenshots/Screenshot_20241128_095737.jpg',
        "Turn left sign6":'img/road-signs/screenshots/Screenshot_20241128_095740.jpg',
        "Turn left sign7":'img/road-signs/screenshots/Screenshot_20241128_095744.jpg',
        "Turn left sign8":'img/road-signs/screenshots/Screenshot_20241128_095750.jpg',
        "Turn left sign9":'img/road-signs/screenshots/Screenshot_20241128_095824.jpg'
    }

    # Load templates
    try:
        templates = load_templates(template_paths)
    except FileNotFoundError as e:
        print(e)
        return

    # Initialize screen capture and QR code detector
    with mss.mss() as sct:
        qr_detector = cv2.QRCodeDetector()
        detected_qr_codes = set()
        monitor = sct.monitors[1]  # Choose the monitor to capture

        print("Starting screen capture and detection...")
        while True:
            # Capture a screenshot
            screenshot = sct.grab(monitor)
            screen_image = numpy.array(screenshot)
            screen_gray = cv2.cvtColor(screen_image, cv2.COLOR_BGR2GRAY)

            # Detect road signs
            try:
                detect_road_signs(screen_gray, templates)
            except:
                print("An exception occurred during road sign detection")

            # Detect QR codes
            try:
                detect_qr_code(screen_gray, qr_detector, detected_qr_codes)
            except:
                print("An exception occurred during QR code detection")


if __name__ == "__main__":
    main()
