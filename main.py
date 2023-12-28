from fastapi import FastAPI, WebSocket
from backend.sql.connection import init_db
from setup import SetUp
from fastapi.staticfiles import StaticFiles
from backend.websockets.websocket_routes import websocket_endpoint

app = FastAPI()
setup = SetUp()

app.mount("/static", StaticFiles(directory="static", html=True), name="static")


@app.on_event("startup")
async def startup_event():
    await init_db()
    setup.initialize_services()


@app.websocket("/ws")
async def handle_websocket(websocket: WebSocket):
    await websocket_endpoint(websocket, setup.websocket_manager, setup.batch_manager)


@app.on_event("shutdown")
async def shutdown_event():
    await setup.close_services()
