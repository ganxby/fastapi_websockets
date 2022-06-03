from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse

import json


async def connect(websocket: WebSocket):
    await websocket.accept()


async def send_response(message: str, websocket: WebSocket):
    await websocket.send_text(message)


app = FastAPI()


@app.get("/", response_class=FileResponse)
async def get():
    return 'templates/handler_template.html'


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await connect(websocket)

    message_number = 1

    try:
        while True:
            data = await websocket.receive_text()
            json_data = json.loads(data)
            json_response = {
                'text': str(message_number) + '. ' + str(json_data['text'])
            }

            await send_response(json.dumps(json_response), websocket)

            message_number += 1

    except WebSocketDisconnect:
        print('disconnect')
