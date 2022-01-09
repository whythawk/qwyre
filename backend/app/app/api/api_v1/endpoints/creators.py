from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


################################################################################
# 'SUMMARY' COMPONENTS
################################################################################


@router.get("/works", response_model=List[schemas.WorkLineSummary])
def read_creator_works(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get works for current creator.
    """
    creator = crud.creator.get(id=current_user.creator, get_raw=True)
    if not creator:
        raise HTTPException(status_code=400, detail="This is not the creator you were looking for.")
    return crud.creator.get_multi_works(db_obj=creator, skip=skip, limit=limit, get_raw=True)


@router.get("/works/{work_id}", response_model=schemas.WorkSummary)
def read_creator_work(
    *,
    db: Session = Depends(deps.get_db),
    work_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get a specific work for current creator.
    """
    creator = crud.creator.get(id=current_user.creator, get_raw=True)
    if not creator:
        raise HTTPException(status_code=400, detail="This is not the creator you were looking for.")
    return crud.creator.get_work(db_obj=creator, work_id=work_id, get_raw=True)


@router.get("/summaries", response_model=List[schemas.CreatorSummary])
def read_creators(skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve active public creators.
    """
    creators = crud.creator.get_multi_public(skip=skip, limit=limit)
    return creators


@router.get("/summary/{creator_id}", response_model=schemas.CreatorSummary)
def read_creator_summary_by_id(creator_id: UUID,) -> Any:
    """
    Get a specific creator by id.
    """
    creator = crud.creator.get(id=creator_id)
    if creator.isPrivate or not creator.isActive or creator.isBanned:
        raise HTTPException(status_code=400, detail="You can't handle the (summarised) truth.")
    return creator


################################################################################
# 'CRUD' COMPONENTS
################################################################################


@router.put("/", response_model=schemas.Creator)
def update_creator_profile(
    *,
    db: Session = Depends(deps.get_db),
    creator_in: schemas.CreatorUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update creator profile.
    """
    if crud.creator._hexify(creator_in.identifier) != crud.creator._hexify(current_user.creator):
        raise HTTPException(status_code=400, detail="This is not the creator you were looking for.")
    creator = crud.creator.update(obj_in=creator_in)
    return creator


@router.put("/toggle-privacy", response_model=schemas.Creator)
def toggle_creator_privacy(*, current_user: models.User = Depends(deps.get_current_active_user),) -> Any:
    """
    Update creator profile.
    """
    creator = crud.creator.get(id=current_user.creator)
    if not creator:
        raise HTTPException(status_code=400, detail="This is not the creator you were looking for.")
    creator = crud.creator.toggle_privacy(db_obj=creator)
    return creator


@router.get("/", response_model=schemas.Creator)
def read_creator_profile(
    db: Session = Depends(deps.get_db), current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current creator.
    """
    creator = crud.creator.get(id=current_user.creator)
    if not creator:
        raise HTTPException(status_code=400, detail="This is not the creator you were looking for.")
    return creator


@router.get("/{creator_id}", response_model=schemas.Creator)
def read_creator_by_id(
    *, creator_id: UUID, current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Get a specific creator by id.
    """
    creator = crud.creator.get(id=creator_id)
    if creator.isPrivate:
        raise HTTPException(status_code=400, detail="You can't handle the truth.")
    return creator

