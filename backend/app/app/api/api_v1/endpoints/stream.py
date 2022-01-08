from fastapi import APIRouter, Depends, WebSocket, status
from starlette.websockets import WebSocketDisconnect
from websockets.exceptions import ConnectionClosedError
from sqlalchemy.orm import Session
from uuid import UUID
import time
import asyncio
import httpx

from app import crud, models, schema_types, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()


async def send_response(*, websocket: WebSocket, response: dict):
    try:
        await websocket.send_json(response)
        return True
    except (WebSocketDisconnect, ConnectionClosedError):
        return False


async def receive_response(*, websocket: WebSocket) -> dict:
    try:
        return await websocket.receive_json()
    except (WebSocketDisconnect, ConnectionClosedError):
        return {}


@router.websocket("/{work_id}")
async def stream_work(*, db: Session = Depends(deps.get_db), work_id: UUID, websocket: WebSocket):
    current_user = None
    creator = None
    bookmark_in = None
    stream_first = None
    wallet_pointer = None
    error_response = False
    last_page = 0
    last_position = 0
    is_closed = False
    # 1. Validate that the work exists
    work = crud.work.get(id=work_id, get_raw=True)
    await websocket.accept()
    if not work:
        response = {"state": "error", "error": "It was the best of works. It was the worst of works. It did not exist."}
        error_response = True
    if not error_response:
        revenue_share = crud.work.get_revenue_share(db_obj=work)
        revenue_pointers = [r.wallet for r in revenue_share if r.wallet]
        last_page = len(work.stream) - 1
        last_position = len(work.stream[last_page]) - 1
        # 2. Initiate websocket response
        data = await websocket.receive_json()
        # 3. Validate creator and if creator has already bookmarked this work
        if data.get("token"):
            # Logged in creator, and can get their existing bookmark, if it exists
            current_user = deps.get_active_websocket_user(db=db, token=data.get("token"))
            if current_user:
                creator = crud.creator.get(id=current_user.creator, get_raw=True)
            if creator:
                bookmark_in = crud.bookmark.get_from_creator(creator_obj=creator, work_obj=work)
            if bookmark_in and (
                not data.get("page")
                or not data.get("position")
                or data.get("page") < bookmark_in.page
                or data.get("position") < bookmark_in.position
            ):
                # Is logged in, has been reading, but - maybe reading from another device - hasn't got their data so far
                stream_first = crud.work.get_stream_first(db_obj=work, bookmark_in=bookmark_in)
        # 4. If not logged in, or doesn't have a bookmark
        if not bookmark_in:
            # Initialise the stream
            stream_first = crud.work.get_stream_first(db_obj=work)
            bookmark_in = schemas.BookmarkCreate(**{"page": stream_first.page, "position": stream_first.position})
            if creator:
                bookmark_in = crud.bookmark.dogear(obj_in=bookmark_in, creator_obj=creator, work_obj=work)
        ########################################################################
        print("OPEN----------------------------------------------------------")
        print(data)
        print("------")
        print(bookmark_in)
        print("------")
        print(stream_first is None)
        print("--------------------------------------------------------------")
        ########################################################################
        # 5. Reader doesn't need to pay or validate for initial stream. They just receive it.
        if stream_first is not None:
            # Send initial stream to the reader
            stream_first = stream_first.as_neo_dict
            stream_first["identifier"] = str(UUID(stream_first["identifier"]))
            response = {"state": "initialise", "data": {"stream": stream_first}}
            success = await send_response(websocket=websocket, response=response)
            if not success:
                is_closed = True
        # 6. From here on, the reader must pay, and must validate.
        wallet_time = time.time()
        read_time = time.time()
        loop_time = time.time()
        while True:
            if is_closed:
                break
            # 7. Close the stream immediately if owned.
            if bookmark_in.isOwned:
                response = {"state": "complete", "data": {}}
                success = await send_response(websocket=websocket, response=response)
                if not success:
                    is_closed = True
                    break
            # 8. Check if we have a receipt for monetization and creator logged in
            #    https://webmonetization.org/docs/receipt-verifier
            if not creator or not data.get("paying") or data.get("receipt") not in revenue_pointers:
                response = {
                    "state": "payment",
                    "error": "Some expect creators to work for 'exposure'. We hope you are not one of them.",
                }
                error_response = True
                break
            # async with httpx.AsyncClient() as client:
            #     receipt = await client.post(f"{settings.COIL_RECEIPT_VERIFIER}", data=data.get("receipt"))
            # This is shit, since I can't proxy the receipt call, so it needs a major fix
            # 9. Trigger a wallet payment pointer event
            if not wallet_pointer or loop_time - wallet_time > 60:
                wallet_pointer = crud.work.get_revenue_choice(parties_in=revenue_share)
                response = {"state": "pointer", "data": {"pointer": wallet_pointer}}
                success = await send_response(websocket=websocket, response=response)
                if not success:
                    is_closed = True
                    break
                wallet_time = time.time()
            # 10. Trigger the stream
            stream = crud.work.get_stream_second(db_obj=work, page=bookmark_in.page, position=bookmark_in.position)
            bookmark_in.page = stream.page
            bookmark_in.position = stream.position
            if not bookmark_in.paid:
                bookmark_in.paid = 1
            else:
                bookmark_in.paid += 1
            crud.bookmark.update(obj_in=bookmark_in, get_raw=True)
            # 11. Check if the reader now owns the work
            if bookmark_in.page >= last_page and bookmark_in.position >= last_position:
                bookmark_in = crud.bookmark.toggle_ownership(obj_in=bookmark_in)
            stream = stream.as_neo_dict
            stream["identifier"] = str(UUID(stream["identifier"]))
            response = {"state": "reading", "data": {"stream": stream}}
            # 12. Ensure 1 second has passed
            if loop_time - read_time < 1:
                await asyncio.sleep(1 - (loop_time - read_time))
                read_time = time.time()
            # 13. Send the stream update
            success = await send_response(websocket=websocket, response=response)
            if not success:
                is_closed = True
                break
            loop_time = time.time()
            # 14. Wait to receive payment, and loop.
            try:
                data = await websocket.receive_json()
            except (WebSocketDisconnect, ConnectionClosedError):
                is_closed = True
                break
        try:
            if error_response:
                # Send the response error message
                await websocket.send_json(response)
            if not is_closed:
                await websocket.close(code=1000)
        except (WebSocketDisconnect, ConnectionClosedError):
            pass
