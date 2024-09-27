import tkinter as tk

# Function to create a transparent overlay
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
    label = tk.Label(root, text="Position this window over the QR code", bg='gray')
    label.pack(anchor='center')

    # Start the overlay window loop
    root.mainloop()

if __name__ == "__main__":
    create_overlay()
