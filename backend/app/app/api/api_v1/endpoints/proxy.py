from typing import Any
from pydantic import AnyHttpUrl
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic.error_wrappers import ValidationError
from sqlalchemy.orm import Session
import httpx
import base64

from app import crud, models, schemas, schema_types
from app.api import deps
from app.core.config import settings


router = APIRouter()

"""
A proxy for the frontend client when hitting cors issues with axios requests. Adjust as required. This version has
a user-login dependency to reduce the risk of leaking the server as a random proxy.
"""


@router.get("/blob/{path:path}")
async def proxy_get_base64_blob_request(*, path: AnyHttpUrl, request: Request,) -> Any:
    try:
        async with httpx.AsyncClient() as client:
            proxy = await client.get(f"{path}")
        content = crud.epub.convert_to_base64(source=proxy.content)
        content = crud.epub.set_mime(source=content)
        response = Response(content=content, status_code=proxy.status_code)
        return response
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.post("/{path:path}")
async def proxy_post_request(
    *, path: AnyHttpUrl, request: Request, current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    # https://www.starlette.io/requests/
    # https://www.python-httpx.org/quickstart/
    # https://github.com/tiangolo/fastapi/issues/1788#issuecomment-698698884
    # https://fastapi.tiangolo.com/tutorial/path-params/#__code_13
    try:
        data = await request.json()
        headers = {
            "Content-Type": request.headers.get("Content-Type"),
            "Authorization": request.headers.get("Authorization"),
        }
        print("____________________________________________________________________________")
        print("POST REQUEST:", f"{path}", headers)
        print("____________________________________________________________________________")
        async with httpx.AsyncClient() as client:
            proxy = await client.post(f"{path}", headers=headers, data=data)
        response = Response(content=proxy.content, status_code=proxy.status_code)
        return response
    except Exception as e:
        print("____________________________________________________________________________")
        print("POST ERROR:", e)
        print("____________________________________________________________________________")
        raise HTTPException(status_code=403, detail=str(e))


@router.get("/{path:path}")
async def proxy_get_request(
    *, path: AnyHttpUrl, request: Request, current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    try:
        headers = {
            "Content-Type": request.headers.get("Content-Type", "application/x-www-form-urlencoded"),
            "Authorization": request.headers.get("Authorization"),
        }
        print("____________________________________________________________________________")
        print("GET REQUEST:", f"{path}", headers)
        print("____________________________________________________________________________")
        async with httpx.AsyncClient() as client:
            proxy = await client.get(f"{path}", headers=headers)
        print("____________________________________________________________________________")
        print("GET RESPONSE:", proxy.content)
        print("____________________________________________________________________________")
        response = Response(content=proxy.content, status_code=proxy.status_code)
        return response
    except Exception as e:
        print("____________________________________________________________________________")
        print("GET:", e)
        print("____________________________________________________________________________")
        raise HTTPException(status_code=403, detail=str(e))

