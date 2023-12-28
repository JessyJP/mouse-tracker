from fastapi import WebSocket

from backend.utils.batch_manager import BatchManager
from backend.utils.camera_handler import CameraHandler
from backend.utils.db_helper_functions import db_add_user
from backend.websockets.websocket_manager import WebSocketManager


async def websocket_endpoint(websocket: WebSocket, websocket_manager: WebSocketManager, batch_manager: BatchManager):
    await websocket.accept()
    connection_id = await websocket_manager.connect(websocket)
    print(connection_id)
    camera = CameraHandler(connection_id)
    if not await camera.check_camera_available():
        print("Camera not available.")

    await db_add_user(connection_id)
    try:
        while True:
            data = await websocket.receive_json()
            if data.get('type') == 'move':
                print(f"Received from {connection_id}: {data}")
                await batch_manager.add_to_batch(connection_id, f'{data["x"]} {data["y"]}')
            elif data.get('type') == 'right-click':
                print(f"Right-click event received from {connection_id}")
                if await camera.capture_image():
                    print("Image captured successfully.")
                else:
                    print("Failed to capture image.")

    except Exception as e:
        print(f"Error in websocket connection {connection_id}: {e}")
    finally:
        await websocket_manager.disconnect(connection_id)
        await batch_manager.handle_disconnect(connection_id)
        await camera.release_camera()
