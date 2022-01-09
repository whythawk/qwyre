from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, WebSocket, status, Cookie, Query
from pydantic import ValidationError
from sqlalchemy.orm import Session
from neomodel import CardinalityViolation
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
                creator = crud.creator.get(id=current_user.creator)
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


@router.websocket("/import")
async def import_work(*, db: Session = Depends(deps.get_db), websocket: WebSocket):
    creator = None
    error_response = False
    await websocket.accept()
    while True:
        # Send a default response
        # response = {"state": "waiting"}
        # await websocket.send_json(response)
        # Begin import
        data = await websocket.receive_json()
        try:
            current_user = deps.get_active_websocket_user(db=db, token=data.get("token"))
            creator = crud.creator.get(id=current_user.creator)
            if not creator:
                raise ValidationError
        except ValidationError:
            response = {"state": "error", "error": "This is not the creator you were looking for."}
            await websocket.send_json(response)
            error_response = True
            break
        # Send the task
        build_task = celery_app.send_task("app.worker.create_or_update_work", args=[data, creator.identifier])
        response = {"state": "received"}
        await websocket.send_json(response)
        while build_task.state == "PENDING":
            response = {"state": "working"}
            await asyncio.sleep(1)
            await websocket.send_json(response)
        # Get the build response and return it
        try:
            response = {"state": "complete", "data": {"identifier": str(UUID(build_task.get()))}}
        except (ValueError, AttributeError):
            response = {"state": "error", "error": "Import failed"}
        await websocket.send_json(response)
        break
    if error_response:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    else:
        await websocket.close(code=1000)


@router.websocket("/import/{work_id}")
async def update_work(*, db: Session = Depends(deps.get_db), work_id: UUID, websocket: WebSocket):
    creator = None
    error_response = False
    await websocket.accept()
    while True:
        # Begin import
        data = await websocket.receive_json()
        try:
            current_user = deps.get_active_websocket_user(db=db, token=data.get("token"))
            creator = crud.creator.get(id=current_user.creator)
            if not creator or creator.isBanned:
                raise ValidationError
        except ValidationError:
            response = {"state": "error", "error": "This is not the creator you were looking for."}
            await websocket.send_json(response)
            error_response = True
            break
        # Send the task
        build_task = celery_app.send_task("app.worker.create_or_update_work", args=[data, creator.identifier, work_id])
        response = {"state": "received"}
        await websocket.send_json(response)
        while build_task.state == "PENDING":
            response = {"state": "working"}
            await asyncio.sleep(1)
            await websocket.send_json(response)
        # Get the build response and return it
        try:
            response = {"state": "complete", "data": {"identifier": str(UUID(build_task.get()))}}
        except (ValueError, AttributeError, ValidationError):
            response = {"state": "error", "error": "Import failed"}
        await websocket.send_json(response)
        break
    if error_response:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    else:
        await websocket.close(code=1000)


@router.get("/contract/{work_id}/offers", response_model=schemas.ContractOffers)
def read_work_contract_and_offers(
    *,
    db: Session = Depends(deps.get_db),
    work_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Read a contract for a work, including offers.
    """
    creator = crud.creator.get(id=current_user.creator, get_raw=True)
    if not creator:
        raise HTTPException(status_code=404, detail="This is not the creator you were looking for.")
    work = crud.work.get(id=work_id, get_raw=True)
    if not work:
        work = crud.work.get_from_metadata(id=work_id, get_raw=True)
    if not work:
        raise HTTPException(
            status_code=404, detail="It was the best of works. It was the worst of works. It did not exist."
        )
    # Can only read if has contributor role of [AUTHOR, MODERATOR]
    can_view = crud.contributor.has_appropriate_rights(
        creator_obj=creator,
        work_obj=work,
        user_obj=current_user,
        roles=[schema_types.ContributorRoleType.AUTHOR, schema_types.ContributorRoleType.MODERATOR,],
    )
    if not can_view:
        raise HTTPException(
            status_code=400, detail="We are ever striving after what is forbidden, and coveting what is denied us."
        )
    return crud.work.get_contract(db_obj=work, get_raw=True)


@router.get("/contract/{work_id}", response_model=schemas.Contract)
def read_work_contract(*, work_id: UUID, current_user: models.User = Depends(deps.get_current_active_user),) -> Any:
    """
    Read a contract for a work.
    """
    creator = crud.creator.get(id=current_user.creator, get_raw=True)
    if not creator:
        raise HTTPException(status_code=404, detail="This is not the creator you were looking for.")
    work = crud.work.get(id=work_id, get_raw=True)
    if not work:
        work = crud.work.get_from_metadata(id=work_id, get_raw=True)
    if not work:
        raise HTTPException(
            status_code=404, detail="It was the best of works. It was the worst of works. It did not exist."
        )
    # Can only read if has contributor role of [AUTHOR, EDITOR, MODERATOR]
    can_view = crud.contributor.has_appropriate_rights(
        creator_obj=creator,
        work_obj=work,
        user_obj=current_user,
        roles=[
            schema_types.ContributorRoleType.AUTHOR,
            schema_types.ContributorRoleType.EDITOR,
            schema_types.ContributorRoleType.MODERATOR,
        ],
    )
    # Or if a contributor to the work contract (e.g. being considered as editor)
    is_contributor = False
    contract = crud.work.get_contract(db_obj=work, get_raw=True)
    if contract and crud.contract.get_party(db_obj=contract, creator_id=creator.identifier):
        is_contributor = True
    if not can_view and not is_contributor:
        raise HTTPException(
            status_code=400, detail="We are ever striving after what is forbidden, and coveting what is denied us."
        )
    return crud.work.get_contract(db_obj=work, get_raw=True)


@router.post("/contract/{work_id}", response_model=schemas.Contract)
def create_work_contract(
    *,
    work_id: UUID,
    contract_in: schemas.ContractCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a contract for a work.
    """
    creator = crud.creator.get(id=current_user.creator, get_raw=True)
    if not creator:
        raise HTTPException(status_code=404, detail="This is not the creator you were looking for.")
    work = crud.work.get(id=work_id, get_raw=True)
    if not work:
        raise HTTPException(
            status_code=404, detail="It was the best of works. It was the worst of works. It did not exist."
        )
    # Can only create if has contributor role of [AUTHOR]
    can_create = crud.contributor.has_appropriate_rights(
        creator_obj=creator, work_obj=work, user_obj=current_user, roles=[schema_types.ContributorRoleType.AUTHOR,],
    )
    if not can_create:
        raise HTTPException(
            status_code=400, detail="We are ever striving after what is forbidden, and coveting what is denied us."
        )
    if crud.work.has_contract(db_obj=work):
        raise HTTPException(
            status_code=400, detail="A contract is only as good as the people signing it. This one already exists."
        )
    contract = crud.contract.create(connect_obj=work, obj_in=contract_in, get_raw=True)
    return contract


@router.put("/contract/{work_id}/publish", response_model=schemas.WorkSummary)
def publish_work_contract(*, work_id: UUID, current_user: models.User = Depends(deps.get_current_active_user),) -> Any:
    """
    Publish or unpublish a contract for a work.
    """
    creator = crud.creator.get(id=current_user.creator, get_raw=True)
    if not creator:
        raise HTTPException(status_code=400, detail="This is not the creator you were looking for.")
    work = crud.work.get(id=work_id, get_raw=True)
    if not work:
        raise HTTPException(
            status_code=404, detail="It was the best of works. It was the worst of works. It did not exist."
        )
    if not crud.work.has_contract(db_obj=work):
        raise HTTPException(
            status_code=400, detail="A contract is only as good as the people signing it. This one does not exist."
        )
    contract = work.contract.single()
    if not crud.contract.has_elevated_rights(creator_obj=creator, contract_obj=contract, user_obj=current_user):
        raise HTTPException(
            status_code=400, detail="We are ever striving after what is forbidden, and coveting what is denied us."
        )
    # Update history
    if schema_types.WorkStateType(work.state) == schema_types.WorkStateType.OFFERED:
        # Withdraw from publication
        history_in = schemas.HistoryCreate(**{"state": schema_types.WorkStateType.SUBMITTED})
    else:
        history_in = schemas.HistoryCreate(**{"state": schema_types.WorkStateType.OFFERED})
    history_obj = crud.history.create(obj_in=history_in, get_raw=True)
    work = crud.work.update_state(db_obj=work, history_obj=history_obj, get_raw=True)
    return work


@router.put("/{work_id}/publish", response_model=schemas.WorkSummary)
def publish_work(*, work_id: UUID, current_user: models.User = Depends(deps.get_current_active_user),) -> Any:
    """
    Publish or unpublish a work.
    """
    creator = crud.creator.get(id=current_user.creator, get_raw=True)
    if not creator:
        raise HTTPException(status_code=400, detail="This is not the creator you were looking for.")
    work = crud.work.get(id=work_id, get_raw=True)
    if not work:
        raise HTTPException(
            status_code=404, detail="It was the best of works. It was the worst of works. It did not exist."
        )
    if not crud.work.has_contract(db_obj=work):
        raise HTTPException(
            status_code=400, detail="A contract is only as good as the people signing it. This one does not exist."
        )
    contract = work.contract.single()
    if not crud.contract.has_elevated_rights(creator_obj=creator, contract_obj=contract, user_obj=current_user):
        raise HTTPException(
            status_code=400, detail="We are ever striving after what is forbidden, and coveting what is denied us."
        )
    # Update history
    if schema_types.WorkStateType(work.state) == schema_types.WorkStateType.PUBLISHED:
        # Withdraw from publication
        history_in = schemas.HistoryCreate(**{"state": schema_types.WorkStateType.EDITED})
    else:
        history_in = schemas.HistoryCreate(**{"state": schema_types.WorkStateType.PUBLISHED})
    history_obj = crud.history.create(obj_in=history_in, get_raw=True)
    work = crud.work.update_state(db_obj=work, history_obj=history_obj, get_raw=True)
    return work


@router.put("/{work_id}", response_model=schemas.WorkSummary)
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
    creator = crud.creator.get(id=current_user.creator, get_raw=True)
    if not creator:
        raise HTTPException(status_code=404, detail="This is not the creator you were looking for.")
    work = crud.work.get(id=work_id, get_raw=True)
    if not work:
        raise HTTPException(
            status_code=404, detail="It was the best of works. It was the worst of works. It did not exist."
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
    work = crud.work.get(id=work_id, get_raw=True)
    return work


@router.get("/{work_id}/auth", response_model=schemas.WorkSummary)
def read_work_metadata(*, work_id: UUID, current_user: models.User = Depends(deps.get_current_active_user),) -> Any:
    """
    Read a work if appropriate authorised.
    """
    creator = crud.creator.get(id=current_user.creator, get_raw=True)
    if not creator:
        raise HTTPException(status_code=404, detail="This is not the creator you were looking for.")
    work = crud.work.get_from_metadata(id=work_id, get_raw=True)
    # work = crud.work.get(id=work_id, get_raw=True)
    if not work:
        raise HTTPException(
            status_code=404, detail="It was the best of works. It was the worst of works. It did not exist."
        )
    # Can only read if has contributor role of [AUTHOR, EDITOR, MODERATOR]
    can_view = crud.contributor.has_appropriate_rights(
        creator_obj=creator,
        work_obj=work,
        user_obj=current_user,
        roles=[
            schema_types.ContributorRoleType.AUTHOR,
            schema_types.ContributorRoleType.EDITOR,
            schema_types.ContributorRoleType.MODERATOR,
        ],
    )
    # Or if a contributor to the work contract (e.g. being considered as editor)
    is_contributor = False
    contract = crud.work.get_contract(db_obj=work, get_raw=True)
    if contract and crud.contract.get_party(db_obj=contract, creator_id=creator.identifier):
        is_contributor = True
    if not can_view and not is_contributor:
        raise HTTPException(
            status_code=400, detail="We are ever striving after what is forbidden, and coveting what is denied us."
        )
    return work


@router.delete("/{work_id}", response_model=schemas.Msg, status_code=201)
def delete_work(*, work_id: UUID, current_user: models.User = Depends(deps.get_current_active_user),) -> Any:
    """
    Delete a work and its resources.
    """
    creator = crud.creator.get(id=current_user.creator, get_raw=True)
    if not creator:
        raise HTTPException(status_code=404, detail="This is not the creator you were looking for.")
    work = crud.work.get(id=work_id, get_raw=True)
    if not work:
        raise HTTPException(
            status_code=404, detail="It was the best of works. It was the worst of works. It did not exist."
        )
    # Can only delete if has contributor role of [AUTHOR, MODERATOR]
    can_delete = crud.contributor.has_appropriate_rights(
        creator_obj=creator,
        work_obj=work,
        user_obj=current_user,
        roles=[schema_types.ContributorRoleType.AUTHOR, schema_types.ContributorRoleType.MODERATOR,],
    )
    if not can_delete:
        raise HTTPException(
            status_code=400, detail="We are ever striving after what is forbidden, and coveting what is denied us."
        )
    crud.work.remove(id=work_id)
    return {"msg": "Some works are not to be tossed aside lightly, but - rather - with great force."}
