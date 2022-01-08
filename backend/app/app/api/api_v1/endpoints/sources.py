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


@router.get("/authenticated/{source_type}/{source_id}", response_model=schemas.BaseSource)
def read_source_if_authenticated(
    *,
    db: Session = Depends(deps.get_db),
    source_type: str,
    source_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get source data in base64.
    """
    try:
        source_type = schema_types.ResourceType(source_type)
    except ValueError:
        raise HTTPException(
            status_code=400, detail="We are ever striving after what is forbidden, and coveting what is denied us."
        )
    work = crud.work.get(id=source_id, get_raw=True)
    creator = crud.creator.get(id=current_user.creator, get_raw=True)
    if not work or not creator:
        raise HTTPException(
            status_code=400, detail="We are ever striving after what is forbidden, and coveting what is denied us."
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
    cover = crud.cover.get(source_id=source_id, cover_type=source_type)
    if not cover:
        raise HTTPException(
            status_code=404, detail="It was the best of covers. It was the worst of covers. It didn't exist."
        )
    source = schemas.BaseSource(**{"data": cover, "name": f"{source_id}.JPG",})
    return source


@router.get("/{source_type}/{cover_id}", response_model=schemas.BaseSource)
def read_cover(*, source_type: str, cover_id: UUID,) -> Any:
    """
    Get a cover image in base64.
    """
    try:
        source_type = schema_types.ResourceType(source_type)
    except ValueError:
        raise HTTPException(
            status_code=400, detail="We are ever striving after what is forbidden, and coveting what is denied us."
        )
    work = crud.work.get(id=cover_id)
    if not work or schema_types.WorkStateType(work.state) not in [
        schema_types.WorkStateType.PUBLISHED,
        schema_types.WorkStateType.OFFERED,
    ]:
        raise HTTPException(
            status_code=400, detail="We are ever striving after what is forbidden, and coveting what is denied us."
        )
    cover = crud.cover.get(source_id=cover_id, cover_type=source_type)
    if not cover:
        raise HTTPException(
            status_code=404, detail="It was the best of covers. It was the worst of covers. It didn't exist."
        )
    source = schemas.BaseSource(**{"data": cover, "name": f"{cover_id}.JPG",})
    return source

