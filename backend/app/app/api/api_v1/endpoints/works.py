from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, WebSocket, status, Cookie, Query
from pydantic import ValidationError
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
import asyncio

from app import crud, models, schema_types, schemas
from app.api import deps
from app.core.celery_app import celery_app

router = APIRouter()


@router.websocket("/create")
async def create_work(*, db: Session = Depends(deps.get_db), websocket: WebSocket):
    creator = None
    identifier = str(uuid4())
    response = {"state": "waiting", "data": {"identifier": identifier}}
    error_response = False
    await websocket.accept()
    while True:
        # Send a default identifier
        await websocket.send_json(response)
        # Begin build
        data = await websocket.receive_json()
        if data.get("token"):
            try:
                current_user = deps.get_active_websocket_user(db=db, token=data.get("token"))
                creator = crud.creator.get(current_user.creator)
            except ValidationError as e:
                response = {"state": "error", "error": e}
                await websocket.send_json(response)
                error_response = True
                break
        # Should have an identifier
        if data.get("metadata", {}).get("identifier"):
            identifier = data["metadata"]["identifier"]
        else:
            response = {"state": "error", "error": "No metadata identifier provided."}
            await websocket.send_json(response)
            error_response = True
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
            response = {"state": "error", "error": "Build failed"}
        await websocket.send_json(response)
        if creator and data.get("save") and response.get("data"):
            # Save the work to the db
            data["work"] = response["data"]["work"]
            data["metadata"]["uid"] = data["metadata"].pop("identifier")
            build_task = celery_app.send_task("app.worker.create_or_update_work", args=[data, creator.identifier])
        break
    if error_response:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    else:
        await websocket.close(code=1000)


@router.put("/{work_id}", response_model=schemas.Work)
def update_work_metadata(
    *,
    db: Session = Depends(deps.get_db),
    work_id: UUID,
    work_in: schemas.WorkMetadata,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update work metadata.
    """
    creator = crud.creator.get(id=current_user.creator)
    if not creator:
        raise HTTPException(status_code=404, detail="This is not the creator you were looking for.")
    work = crud.work.get(id=work_id)
    if not work:
        raise HTTPException(
            status_code=404, detail="It was the best of works. It was the worst of works. It didn't exist."
        )
    # Can only edit if has contributor role of [AUTHOR, EDITOR, MODERATOR]
    can_edit = crud.contributor.has_appropriate_rights(
        creator_obj=creator,
        work_obj=work,
        user_obj=current_user,
        roles=[
            schema_types.ContributorRoleType.AUTHOR,
            schema_types.ContributorRoleType.EDITOR,
            schema_types.ContributorRoleType.MODERATOR,
        ],
    )
    if not can_edit:
        raise HTTPException(
            status_code=400, detail="We are ever striving after what is forbidden, and coveting what is denied us."
        )
    work_metadata = work_in.dict(exclude_unset=True)
    work_metadata["identifier"] = work.metadata.identifier
    work_metadata_in = schemas.WorkMetadataUpdate(**work_metadata)
    crud.work_metadata.update(obj_in=work_metadata_in)
    work = crud.work.get(id=work_id)
    return work


@router.put("/{work_id}/dedication", response_model=schemas.Work)
def update_work_dedication(
    *,
    db: Session = Depends(deps.get_db),
    work_id: UUID,
    dedication_in: List[str],
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update work metadata.
    """
    creator = crud.creator.get(current_user.creator)
    if not creator:
        raise HTTPException(status_code=404, detail="This is not the creator you were looking for.")
    work = crud.work.get(work_id)
    if not work:
        raise HTTPException(
            status_code=404, detail="It was the best of works. It was the worst of works. It didn't exist."
        )
    # Can only edit if has contributor role of [AUTHOR, EDITOR, MODERATOR]
    can_edit = crud.contributor.has_appropriate_rights(
        creator_obj=creator,
        work_obj=work,
        user_obj=current_user,
        roles=[
            schema_types.ContributorRoleType.AUTHOR,
            schema_types.ContributorRoleType.EDITOR,
            schema_types.ContributorRoleType.MODERATOR,
        ],
    )
    if not can_edit:
        raise HTTPException(
            status_code=400, detail="We are ever striving after what is forbidden, and coveting what is denied us."
        )
    # history_in = schemas.HistoryCreate(**{
    #     "state": schema_types.WorkStateType.
    # })
    work_in = schemas.WorkUpdate(**{"identifier": work_id, "dedication": dedication_in})
    work = crud.work.update(obj_in=work_in)
    return work
