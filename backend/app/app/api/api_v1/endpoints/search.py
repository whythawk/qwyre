from typing import Any, List, Optional
from fastapi import APIRouter, Query


from app import crud, schemas

router = APIRouter()


@router.get("/", response_model=List[schemas.SearchSummary])
def read_search_results(q: Optional[str] = Query(None, max_length=50)) -> Any:
    """
    Get search results.
    """
    if not q:
        return crud.search.get_random()
    return crud.search.get_search_results(query=q)


@router.get("/suggestions/", response_model=List[str])
def read_search_suggestions(q: Optional[str] = Query(None, max_length=50, min_length=2)) -> Any:
    """
    Get search suggestions.
    """
    return crud.search.get_search_suggestions(query=q)
