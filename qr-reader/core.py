import mss
import numpy
import cv2
# from win10toast import ToastNotifier

# toaster = ToastNotifier()

def capture_screen_and_detect_qr():
    qr_codes = set()

    # Capture screen
    with mss.mss() as sct:
        monitor = sct.monitors[1] # You can choose which monitor to capture
        qr_detector = cv2.QRCodeDetector()

        while True:
            # print("QR code search started...")
            screenshot = sct.grab(monitor)
            img = numpy.array(screenshot) # Convert to numpy array
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Convert to grayscale

            qr_code, points, _ = qr_detector.detectAndDecode(img) # Detect and decode QR code
            if points is not None and qr_code and qr_code not in qr_codes:
                qr_codes.add(qr_code)
                print(f"New QR code detected: {qr_codes}")

                # print(f"QR Code detected: {data}")
                # toaster.show_toast("QR Code Detected", data, duration=5)

# Run the application
capture_screen_and_detect_qr()
