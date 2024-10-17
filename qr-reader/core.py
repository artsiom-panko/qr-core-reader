import mss
import numpy
import cv2
import winsound

def capture_screen_and_detect_qr():
    qr_codes = set()

    # Capture screen
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        qr_detector = cv2.QRCodeDetector()

        while True:
            screenshot = sct.grab(monitor)

            img = numpy.array(screenshot) # Convert to numpy array
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Convert to grayscale

            qr_code, points, _ = qr_detector.detectAndDecode(img) # Detect and decode QR code

            if points is not None and qr_code and qr_code not in qr_codes:
                qr_codes.add(qr_code)
                print(f"New QR code detected: {qr_codes}")
                winsound.PlaySound("rooster.wav", winsound.SND_FILENAME)

# Run the application
capture_screen_and_detect_qr()
