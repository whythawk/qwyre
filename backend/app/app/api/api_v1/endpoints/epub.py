from fastapi import APIRouter, WebSocket
from uuid import uuid4
import asyncio

from app.core.celery_app import celery_app


router = APIRouter()


@router.websocket("/build")
async def build_endpoint(websocket: WebSocket):
    identifier = str(uuid4())
    response = {"state": "waiting", "data": {"identifier": identifier}}
    await websocket.accept()
    while True:
        # Send a default identifier
        await websocket.send_json(response)
        # Begin build
        data = await websocket.receive_json()
        # Should have an identifier
        if data.get("metadata", {}).get("identifier"):
            identifier = data["metadata"]["identifier"]
        else:
            response["state"] = "error"
            response["error"] = "No metadata identifier provided."
            await websocket.send_json(response)
            break
        # Send the task
        build_task = celery_app.send_task("app.worker.build_epub", args=[data, identifier])
        response["state"] = "received"
        await websocket.send_json(response)
        while build_task.state == "PENDING":
            response["state"] = "building"
            await asyncio.sleep(1)
            await websocket.send_json(response)
        # Get the build response and return it
        response["state"] = "complete"
        response["data"]["work"] = build_task.get()
        if response["data"]["work"] == "Build failed":
            response["state"] = "error"
            response["error"] = "Build failed"
        await websocket.send_json(response)
        break
    await websocket.close(code=1000)
