import uuid
from fastapi import WebSocket


class WebSocketManager:
    def __init__(self):
        self._active_connections = {}

    async def connect(self, websocket: WebSocket):
        connection_id = str(uuid.uuid4())
        self._active_connections[connection_id] = websocket
        return connection_id

    async def disconnect(self, connection_id: str):
        if connection_id in self._active_connections:
            del self._active_connections[connection_id]

    # async def send_message(self, message: str, connection_id: str):
    #     if connection_id in self._active_connections:
    #         websocket = self._active_connections[connection_id]
    #         await websocket.send_json(message)
    #
    # async def broadcast(self, message: str):
    #     for websocket in self._active_connections.values():
    #         await websocket.send_json(message)
