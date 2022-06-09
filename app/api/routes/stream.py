from fastapi import WebSocket, APIRouter
import pybase64
import asyncio

from app.services.launcher import q_output, stop, run


router = APIRouter()


@router.websocket("/")
async def stream(websocket: WebSocket):
    run()
    await websocket.accept()
    try:
        while True:
            if not q_output.empty():
                frame = pybase64.b64encode_as_string(q_output.get_nowait())
                await websocket.send_text(f"data:image/jpeg;base64, {frame}")
                try:
                    await asyncio.wait_for(websocket.receive(), 0.01)
                except asyncio.TimeoutError:
                    ...
    except RuntimeError:
        stop()

