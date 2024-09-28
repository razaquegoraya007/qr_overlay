import tkinter as tk
import requests
from pyzbar import pyzbar
from PIL import ImageGrab  # To capture the screen
import cv2
import numpy as np

# Function to send QR code data to the website
def send_qr_data_to_website(data, url="http://127.0.0.1:5000/qr"):
    payload = {'qr_code': data}
    try:
        print(f"[DEBUG] Sending POST request to {url} with payload: {payload}")
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"[INFO] Data sent successfully: {data}")
        else:
            print(f"[ERROR] Failed to send data. Server responded with: {response.status_code}")
        return response.status_code
    except Exception as e:
        print(f"[ERROR] Error sending data: {e}")
        return None

# Function to detect QR codes in the captured image
def detect_qr_codes_in_image(image):
    frame = np.array(image)  # Convert the PIL image to a NumPy array
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convert RGB to BGR for OpenCV

    qr_codes = pyzbar.decode(frame)
    print(f"[DEBUG] Detecting QR codes: Found {len(qr_codes)}")

    if len(qr_codes) == 0:
        print("[INFO] No QR codes detected. Make sure the QR code is visible and properly positioned.")
    else:
        for qr_code in qr_codes:
            data = qr_code.data.decode("utf-8")
            print(f"[INFO] QR Code detected: {data}")
            send_qr_data_to_website(data)  # Send detected QR code to the server

    return qr_codes

# Function to capture a region of the screen
def capture_screen(overlay_position):
    x1, y1, x2, y2 = overlay_position
    # Capture the area of the screen under the overlay window
    image = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    return image

# Function to start the screen capture and QR detection
def start_qr_detection(overlay_position):
    while True:
        # Capture the screen where the overlay is positioned
        image = capture_screen(overlay_position)

        # Display the captured image for debugging purposes
        cv2.imshow("Captured Screen Area", np.array(image))

        # Detect QR codes in the captured image
        detect_qr_codes_in_image(image)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

# Create a transparent overlay window
def create_overlay():
    root = tk.Tk()
    root.geometry("300x300")  # Initial window size
    root.title("QR Code Scanner Overlay")

    # Make window always on top and set opacity (alpha value)
    root.wm_attributes("-topmost", True)
    root.wm_attributes("-alpha", 0.3)  # Set transparency (0.0 fully transparent to 1.0 fully opaque)

    # Allow resizing and moving
    root.resizable(True, True)

    # Instructions Label
    label = tk.Label(root, text="Position this window over the QR code on your screen", bg='gray')
    label.pack(anchor='center')

    def on_close():
        # Get the position of the overlay window and pass it to the QR scanner
        overlay_position = root.winfo_x(), root.winfo_y(), root.winfo_x() + root.winfo_width(), root.winfo_y() + root.winfo_height()
        root.destroy()  # Close the overlay window
        start_qr_detection(overlay_position)

    # Trigger QR scanning when the overlay is closed
    root.protocol("WM_DELETE_WINDOW", on_close)

    # Start the overlay window loop
    root.mainloop()

if __name__ == "__main__":
    create_overlay()
