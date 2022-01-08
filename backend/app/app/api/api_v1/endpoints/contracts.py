from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app import crud, models, schema_types, schemas
from app.api import deps
from app.schema_types.work_state_types import WorkStateType
from app.utilities import (
    send_expression_of_interest_confirmation_email,
    send_expression_of_interest_email,
)

router = APIRouter()


@router.get("/", response_model=List[schemas.Contract])
def read_creator_contracts(
    *, skip: int = 0, limit: int = 100, current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get contracts for current creator.
    """
    creator = crud.creator.get(id=current_user.creator, get_raw=True)
    if not creator:
        raise HTTPException(status_code=400, detail="This is not the creator you were looking for.")
    return crud.contract.get_multi_as_party(db_obj=creator, skip=skip, limit=limit, get_raw=True)


@router.get("/offers", response_model=List[schemas.Contract])
def read_offered_contracts(*, skip: int = 0, limit: int = 100) -> Any:
    """
    Get contracts for current creator.
    """
    return crud.contract.get_multi_by_offered(skip=skip, limit=limit, get_raw=True)


@router.get("/offers/{contract_id}", response_model=schemas.Contract)
def read_offered_contract(*, contract_id: UUID) -> Any:
    """
    Get contracts for current creator.
    """
    contract = crud.contract.get(id=contract_id, get_raw=True)
    if not contract:
        raise HTTPException(
            status_code=400, detail="A contract is only as good as the people signing it. This one doesn't exist."
        )
    if not crud.work.has_state(db_obj=contract.work.single(), state=schema_types.WorkStateType.OFFERED):
        raise HTTPException(
            status_code=400, detail="We are ever striving after what is forbidden, and coveting what is denied us."
        )
    return contract


@router.post("/offers/{contract_id}/express-interest", response_model=schemas.Msg, status_code=201)
def express_interest_in_offered_contract(
    *,
    db: Session = Depends(deps.get_db),
    contract_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Express interest in an offered contract for current creator.
    """
    creator = crud.creator.get(id=current_user.creator, get_raw=True)
    if not creator:
        raise HTTPException(status_code=400, detail="This is not the creator you were looking for.")
    contract = crud.contract.get(id=contract_id, get_raw=True)
    if not contract:
        raise HTTPException(
            status_code=400, detail="A contract is only as good as the people signing it. This one doesn't exist."
        )
    work = contract.work.single()
    emails = crud.user.get_emails_for_creators(db=db, creator_objs=work.metadata.single().creator.all())
    if (
        not crud.work.has_state(db_obj=work, state=schema_types.WorkStateType.OFFERED)
        or not crud.creator.can_make_offers(db_obj=creator, user_obj=current_user)
        or crud.work.is_work_creator(db_obj=work, creator_obj=creator)
        or not emails
    ):
        raise HTTPException(
            status_code=400, detail="We are ever striving after what is forbidden, and coveting what is denied us."
        )
    # Send the emails
    data = schemas.ConfirmExpressionOfInterest(
        **{
            "email": current_user.email,
            "subject": f"Confirmation of your interest in '{work.metadata.single().title}'",
            "contract_link": f"/offers/{contract.identifier}",
            "workspace_link": "/workshop",
            "work_title": work.metadata.single().title,
        }
    )
    send_expression_of_interest_confirmation_email(data=data)
    data = schemas.ReceiveExpressionOfInterest(
        **{
            "emails": emails,
            "subject": f"Someone is interested in editing '{work.metadata.single().title}'",
            "contract_link": f"/offers/{contract.identifier}",
            "workspace_link": "/workshop",
            "work_title": work.metadata.single().title,
            "creator_link": f"/creator/{creator.identifier}",
            "creator": crud.creator.creator_name(db_obj=creator),
            "creator_email": current_user.email,
        }
    )
    send_expression_of_interest_email(data=data)
    # Connect the offer to the contract
    crud.creator.add_contract_offer(db_obj=creator, contract_obj=contract)
    return {"msg": "We have expressed your interest. Check your email for further details."}


@router.post("/offers/{contract_id}/editor/{editor_id}/reject", response_model=schemas.Contract)
def reject_contract_editor_offer(
    *, contract_id: UUID, editor_id: UUID, current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Reject an offer to edit for a contract for a specified creator.
    """
    creator = crud.creator.get(id=current_user.creator, get_raw=True)
    if not creator:
        raise HTTPException(status_code=400, detail="This is not the creator you were looking for.")
    editor = crud.creator.get(id=editor_id, get_raw=True)
    if not editor:
        raise HTTPException(status_code=400, detail="This is not the editor you were looking for.")
    contract = crud.contract.get(id=contract_id, get_raw=True)
    if not contract:
        raise HTTPException(
            status_code=400, detail="A contract is only as good as the people signing it. This one doesn't exist."
        )
    work = contract.work.single()
    if (
        not crud.work.has_state(db_obj=work, state=schema_types.WorkStateType.OFFERED)
        or not crud.creator.can_make_offers(db_obj=creator, user_obj=current_user)
        or not crud.work.is_work_creator(db_obj=work, creator_obj=creator)
        # or not crud.creator.can_assign_parties(db_obj=contract)
    ):
        raise HTTPException(
            status_code=400, detail="We are ever striving after what is forbidden, and coveting what is denied us."
        )
    # Do the removals of the offer to the contract, including if the editor has already been assigned to the contract
    crud.creator.remove_contract_offer(db_obj=editor, contract_obj=contract)
    party = crud.contract.get_party(db_obj=contract, creator_id=editor_id)
    if party:
        crud.contract.remove_party(db_obj=party)
    contract = crud.contract.get(id=contract_id, get_raw=True)
    return contract


@router.post("/offers/{contract_id}/editor/{editor_id}/accept", response_model=schemas.Contract)
def accept_contract_editor_offer(
    *, contract_id: UUID, editor_id: UUID, current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Accept an offer to edit for a contract for a specified creator.
    """
    creator = crud.creator.get(id=current_user.creator, get_raw=True)
    if not creator:
        raise HTTPException(status_code=400, detail="This is not the creator you were looking for.")
    editor = crud.creator.get(id=editor_id, get_raw=True)
    if not editor:
        raise HTTPException(status_code=400, detail="This is not the editor you were looking for.")
    contract = crud.contract.get(id=contract_id, get_raw=True)
    if not contract:
        raise HTTPException(
            status_code=400, detail="A contract is only as good as the people signing it. This one doesn't exist."
        )
    work = contract.work.single()
    if (
        not crud.work.has_state(db_obj=work, state=schema_types.WorkStateType.OFFERED)
        or not crud.creator.can_make_offers(db_obj=creator, user_obj=current_user)
        or not crud.work.is_work_creator(db_obj=work, creator_obj=creator)
        or not crud.contract.can_assign_parties(db_obj=contract)
    ):
        raise HTTPException(
            status_code=400, detail="We are ever striving after what is forbidden, and coveting what is denied us."
        )
    # Do the assignments
    contract = crud.contract.add_party(db_obj=contract, creator_obj=editor, get_raw=True)
    return contract


@router.get("/contributions", response_model=List[schemas.Contract])
def read_contracts_as_party_contributor(
    *, skip: int = 0, limit: int = 100, current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get contracts for current creator where they are contributor, not creator.
    """
    creator = crud.creator.get(id=current_user.creator, get_raw=True)
    if not creator:
        raise HTTPException(status_code=400, detail="This is not the creator you were looking for.")
    return crud.contract.get_multi_as_party(creator_obj=creator, skip=skip, limit=limit, get_raw=True)


@router.post("/{contract_id}/approve", response_model=schemas.Contract)
def toggle_party_contract_approval(
    *, contract_id: UUID, current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Toggle approval (signature) of a contract by the current creator.
    """
    creator = crud.creator.get(id=current_user.creator, get_raw=True)
    if not creator:
        raise HTTPException(status_code=400, detail="This is not the creator you were looking for.")
    contract = crud.contract.get(id=contract_id, get_raw=True)
    if not contract:
        raise HTTPException(
            status_code=400, detail="A contract is only as good as the people signing it. This one doesn't exist."
        )
    # Check if a change to the contract can be made (i.e. if the contract itself has already been signed by all parties
    # no further changes may be made.)
    if contract.isApproved:
        raise HTTPException(status_code=400, detail="Mez quant ja est la chose fecte, ne peut pas bien estre desfecte.")
    party = crud.contract.get_party(db_obj=contract, creator_id=creator.identifier)
    if not party:
        raise HTTPException(
            status_code=400, detail="We are ever striving after what is forbidden, and coveting what is denied us."
        )
    # Contract exists, contract can be signed, and creator is a party to the contract
    contract = crud.contract.toggle_party_contract_approval(contract_obj=contract, party_obj=party, get_raw=True)
    if contract.isApproved:
        # Update the work status to CONTRACTED
        work = crud.contract.get_work(db_obj=contract)
        if not work:
            raise HTTPException(
                status_code=404, detail="It was the best of works. It was the worst of works. It did not exist."
            )
        history_in = schemas.HistoryCreate(**{"state": schema_types.WorkStateType.CONTRACTED})
        history_obj = crud.history.create(obj_in=history_in, get_raw=True)
        work = crud.work.update_state(db_obj=work, history_obj=history_obj, get_raw=True)
    return contract


@router.post("/{contract_id}/publish", response_model=schemas.Contract)
def toggle_party_contract_publication(
    *, contract_id: UUID, current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Toggle approval (signature) of a contract by the current creator.
    """
    creator = crud.creator.get(id=current_user.creator, get_raw=True)
    if not creator:
        raise HTTPException(status_code=400, detail="This is not the creator you were looking for.")
    contract = crud.contract.get(id=contract_id, get_raw=True)
    if not contract:
        raise HTTPException(
            status_code=400, detail="A contract is only as good as the people signing it. This one doesn't exist."
        )
    # Check if a change to the contract can be made (i.e. if the contract itself has not been signed by all parties
    # the work cannot be published, and if it is already published, it cannot be unpublished.)
    # A fully signed and executed contract cannot be unilaterally changed by any of the parties.
    if not contract.isApproved:
        raise HTTPException(
            status_code=400, detail="Mez quant ja est la chose pas fecte, ne peut pas bien estre fecte."
        )
    if contract.publicationApproved:
        raise HTTPException(status_code=400, detail="Mez quant ja est la chose fecte, ne peut pas bien estre desfecte.")
    party = crud.contract.get_party(db_obj=contract, creator_id=creator.identifier)
    if not party:
        raise HTTPException(
            status_code=400, detail="We are ever striving after what is forbidden, and coveting what is denied us."
        )
    # Contract exists, contract can be executed, and creator is a party to the contract
    contract = crud.contract.toggle_party_contract_publication(contract_obj=contract, party_obj=party, get_raw=True)
    if contract.publicationApproved:
        # Update the work status to EDITED
        work = crud.contract.get_work(db_obj=contract)
        if not work:
            raise HTTPException(
                status_code=404, detail="It was the best of works. It was the worst of works. It did not exist."
            )
        history_in = schemas.HistoryCreate(**{"state": schema_types.WorkStateType.EDITED})
        history_obj = crud.history.create(obj_in=history_in, get_raw=True)
        work = crud.work.update_state(db_obj=work, history_obj=history_obj, get_raw=True)
    return contract


@router.put("/{contract_id}", response_model=schemas.Contract)
def update_contract(
    *,
    contract_id: UUID,
    contract_in: schemas.ContractUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a contract for a work.
    """
    creator = crud.creator.get(id=current_user.creator, get_raw=True)
    if not creator:
        raise HTTPException(status_code=400, detail="This is not the creator you were looking for.")
    contract = crud.contract.get(id=contract_id, get_raw=True)
    if not contract:
        raise HTTPException(
            status_code=400, detail="A contract is only as good as the people signing it. This one doesn't exist."
        )
    if (
        not crud.contract.has_elevated_rights(creator_obj=creator, contract_obj=contract, user_obj=current_user)
        or contract.isApproved
    ):
        raise HTTPException(
            status_code=400, detail="We are ever striving after what is forbidden, and coveting what is denied us."
        )
    contract = crud.contract.update(obj_in=contract_in, get_raw=True)
    return contract


@router.get("/{contract_id}", response_model=schemas.Contract)
def read_creator_contract(
    *, contract_id: UUID, current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get contracts for current creator.
    """
    creator = crud.creator.get(id=current_user.creator, get_raw=True)
    if not creator:
        raise HTTPException(status_code=400, detail="This is not the creator you were looking for.")
    contract = crud.contract.get(id=contract_id, get_raw=True)
    if not contract:
        raise HTTPException(
            status_code=400, detail="A contract is only as good as the people signing it. This one doesn't exist."
        )
    if not crud.contract.has_appropriate_rights(creator_obj=creator, contract_obj=contract, user_obj=current_user):
        raise HTTPException(
            status_code=400, detail="We are ever striving after what is forbidden, and coveting what is denied us."
        )
    return contract

