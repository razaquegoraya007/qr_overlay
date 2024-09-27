import cv2
from pyzbar import pyzbar
import requests

# Function to send QR code data to the website
def send_qr_data_to_website(data, url="http://127.0.0.1:5000/qr"):
    payload = {'qr_code': data}
    try:
        # POST request
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"[INFO] Data sent successfully: {data}")
        else:
            print(f"[ERROR] Failed to send data. Server responded with: {response.status_code}")
        return response.status_code
    except Exception as e:
        print(f"[ERROR] Error sending data: {e}")
        return None

# Function to detect QR codes in a frame
def detect_qr_codes(frame):
    qr_codes = pyzbar.decode(frame)
    detected_codes = []
    for qr_code in qr_codes:
        data = qr_code.data.decode("utf-8")
        detected_codes.append(data)

        # Draw rectangle around the QR code
        (x, y, w, h) = qr_code.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        print(f"QR Code detected: {data}")
    return detected_codes

# Function to start the camera and scan for QR codes
def start_qr_scanner(url="http://127.0.0.1:5000/qr"):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("[ERROR] Camera initialization failed")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to capture image")
            break

        # Detect QR codes in the current frame
        qr_codes = detect_qr_codes(frame)

        # Send each detected QR code to the server
        for code in qr_codes:
            send_qr_data_to_website(code, url)

        # Display the camera feed
        cv2.imshow("QR Code Scanner", frame)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_qr_scanner()
