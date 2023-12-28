import asyncio
from datetime import datetime
import cv2
import os
import shutil
from backend.utils.db_helper_functions import db_add_picture_path


class CameraHandler:
    def __init__(self, user_uuid: str, camera_index=0, default_folder=None):
        self.camera_index = camera_index
        self.user_uuid = user_uuid
        self.cap = None

        # Determine the base folder for storing pictures
        script_dir = os.path.dirname(__file__)  # Directory of this script
        base_folder = os.path.join(script_dir, "..", "pictures")
        base_folder = os.path.normpath(base_folder)  # Normalize the path

        # Create a user-specific folder within the base folder
        self.user_folder = os.path.join(base_folder, self.user_uuid)
        if not os.path.exists(self.user_folder):
            os.makedirs(self.user_folder)

    async def capture_image(self):
        if not self.cap or not self.cap.isOpened():
            print("Camera not initialized or not available.")
            return False

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_name = f"{timestamp}.jpg"
        image_path = os.path.join(self.user_folder, image_name)
        await db_add_picture_path(self.user_uuid, image_path)
        return await asyncio.to_thread(self._capture_and_save_image, image_path)

    def _capture_and_save_image(self, image_path):
        ret, frame = self.cap.read()
        if ret:
            try:
                cv2.imwrite(image_path, frame)
                print(f"Image captured and saved as {image_path}")
                return True
            except Exception as e:
                print(f"Error saving image: {e}")
                return False
        else:
            print("Failed to capture image from camera.")
            return False

    async def check_camera_available(self):
        return await asyncio.to_thread(self._open_camera)

    def _open_camera(self):
        self.cap = cv2.VideoCapture(self.camera_index)
        if self.cap is None or not self.cap.isOpened():
            print("No webcam found.")
            return False
        return True

    async def release_camera(self):
        if self.cap:
            await asyncio.to_thread(self.cap.release)
        # Remove user folder if it is empty
        if os.path.exists(self.user_folder) and not os.listdir(self.user_folder):
            shutil.rmtree(self.user_folder)
