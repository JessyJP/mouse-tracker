import tkinter as tk
import uuid

class MouseTrackerAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mouse Tracker")

        # Set window size to 800x700 pixels
        self.root.geometry("800x700")

        # Generate a session ID
        self.session_id = uuid.uuid4()

        # Create a label for the static text
        self.title_label = tk.Label(self.root, text="Move your mouse around within the Window")
        self.title_label.pack()

        # Create a label for the session ID
        self.session_label = tk.Label(self.root, text=f"ID: {self.session_id}")
        self.session_label.pack()

        # Create a label for the coordinates
        self.coordinates_label = tk.Label(self.root, text="Coordinates: ")
        self.coordinates_label.pack()

        # Bind the motion event
        self.root.bind('<Motion>', self.motion)

    def motion(self, event):
        x, y = event.x, event.y
        self.coordinates_label.config(text=f"Coordinates: ({x}, {y})")

def start_application():
    root = tk.Tk()
    app = MouseTrackerAppGUI(root)
    root.mainloop()
