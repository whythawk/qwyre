from fastapi import APIRouter, WebSocket
from uuid import uuid4
from typing import Optional
from pydantic import BaseModel, Field, ValidationError
import asyncio
from app.core.celery_app import celery_app
from chapisha import WorkMetadata
from starlette.websockets import WebSocketDisconnect


class BuildData(BaseModel):
	metadata: WorkMetadata = Field(...)
	cover: str = Field(...)
	text: str = Field(...)
	dedication: Optional[list[str]] = Field(None)


router = APIRouter()


@router.websocket("/build")
async def build_endpoint(websocket: WebSocket):
	await websocket.accept()
	num = 0
	data = False
	while True:
		if not data:
			data = await BuildData(websocket.receive_json())
			print("====================== DATA RECEIVED ======================")
		await asyncio.sleep(1)
		num += 1
		await websocket.send_text(f"Current count: {num}")
		if num > 5 and data:
			break
	await websocket.close(code=1000)

@router.websocket("/ws3")
async def websocket_endpoint3(websocket: WebSocket):
	await websocket.accept()
	print("====================== /ws3 DATA ACCEPTED ======================")
	num = 0
	data = False
	while True:
		if not data:
			data = await websocket.receive_json()
			data = BuildData(**data)
			# print(data)
			print("====================== /ws3 DATA RECEIVED ======================")
		await asyncio.sleep(1)
		num += 1
		response = {"state": "waiting", "data": {"identifier": str(uuid4())}}
		response["data"]["state"] = "error"
		response["data"]["error"] = f"Current count: {num}"
		await websocket.send_json(response)
		# await websocket.send_text(f"Current count: {num}")
		break
	await websocket.close(code=1000)

@router.websocket("/ws2")
async def websocket_endpoint2(websocket: WebSocket):
	await websocket.accept()
	print("====================== /ws2 DATA ACCEPTED ======================")
	num = 0
	data = False
	while True:
		if not data:
			data = await websocket.receive_text()
			print("====================== /ws2 DATA RECEIVED ======================")
		await asyncio.sleep(1)
		num += 1
		await websocket.send_text(f"Current count: {num} | data: {data}")
		if num > 5 and data:
			break
	await websocket.close(code=1000)

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
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
