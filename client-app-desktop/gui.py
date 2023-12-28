import tkinter as tk
import tkinter.ttk as ttk
import uuid
import cv2
from PIL import Image, ImageTk
import platform
import subprocess

class MouseTrackerAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mouse Tracker")
        self.root.geometry("800x700")
        self.session_id = uuid.uuid4()

        # UI setup
        self.title_label = tk.Label(self.root, text="Move your mouse around within the Window")
        self.title_label.pack()

        self.session_label = tk.Label(self.root, text=f"ID: {self.session_id}")
        self.session_label.pack()

        self.coordinates_label = tk.Label(self.root, text="Coordinates: ")
        self.coordinates_label.pack()

        self.root.bind('<Motion>', self.motion)

        # Video devices dropdown
        self.video_devices = self.fetch_video_devices()
        self.video_device_var = tk.StringVar()
        self.video_device_dropdown = ttk.Combobox(self.root, textvariable=self.video_device_var, state="readonly")
        self.video_device_dropdown['values'] = self.video_devices if self.video_devices else ["== NO video devices available =="]
        self.video_device_dropdown.current(0)
        self.video_device_dropdown.pack()

        # Image label for displaying captured image
        self.image_label = tk.Label(self.root)
        self.image_label.pack()

        # Right-click event to capture image
        self.root.bind('<Button-3>', self.capture_image)

    def fetch_video_devices(self):
        if platform.system() == "Windows":
            # Windows-specific code using OpenCV
            # return self.fetch_video_devices_windows()
            return self.fetch_video_devices_opencv()
        elif platform.system() == "Linux":
            # Linux-specific code using v4l2-ctl
            return self.fetch_video_devices_linux()
        else:
            # For other OSes or if no method is available
            return ["No method to fetch devices on this OS"]

    def fetch_video_devices_opencv(self):
        # This function attempts to open video capture devices
        # sequentially and adds them to the list if successful.
        video_devices = []
        max_devices_to_check = 10  # You can adjust this number based on expected devices

        for index in range(max_devices_to_check):
            cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)  # Using CAP_DSHOW for Windows
            if cap.isOpened():
                video_devices.append(f"Camera {index}")
                cap.release()
            else:
                break  # Stop searching if a camera index is not found

        return video_devices

    def fetch_video_devices_windows():
        device_names = []
        wmi_service = win32com.client.Dispatch("WbemScripting.SWbemLocator")
        wmi_winmgmts_root = wmi_service.ConnectServer(".", "root\cimv2")
        col_items = wmi_winmgmts_root.ExecQuery("SELECT * FROM Win32_PnPEntity WHERE Service = 'usbvideo'")
        for obj_item in col_items:
            device_names.append(obj_item.Caption)
        return device_names

    def fetch_video_devices_linux(self):
        # Linux-specific method to list video devices
        try:
            result = subprocess.run(['v4l2-ctl', '--list-devices'], capture_output=True, text=True, check=True)
            devices = result.stdout.split('\n\n')
            return [device.split('\n')[0] for device in devices if device]
        except subprocess.CalledProcessError:
            return []

    def capture_image(self, event):
        # Check if there are available devices
        if not self.video_devices or self.video_device_var.get() == "== NO video devices available ==":
            print("No video devices available.")
            return

        # Get the index of the selected camera
        camera_index = self.video_devices.index(self.video_device_var.get())
        
        capture = cv2.VideoCapture(camera_index)
        
        # Check if the camera opened successfully
        if not capture.isOpened():
            print("Unable to open the camera.")
            capture.release()
            return

        ret, frame = capture.read()
        if ret:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.image_label.imgtk = imgtk
            self.image_label.configure(image=imgtk)
        capture.release()

    def motion(self, event):
        x, y = event.x, event.y
        self.coordinates_label.config(text=f"Coordinates: ({x}, {y})")

def start_application():
    root = tk.Tk()
    app = MouseTrackerAppGUI(root)
    root.mainloop()
