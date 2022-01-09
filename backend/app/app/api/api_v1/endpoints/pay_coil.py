from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
import httpx

from app import crud, models, schemas, schema_types
from app.api import deps
from app.core.config import settings


router = APIRouter()
coil_uri = settings.COIL_URI
coil_api_uri = settings.COIL_API_URI


@router.post("/proxy/{path:path}")
async def proxy_post_request(*, path: str, request: Request) -> Any:
    # https://www.starlette.io/requests/
    # https://www.python-httpx.org/quickstart/
    # https://github.com/tiangolo/fastapi/issues/1788#issuecomment-698698884
    # https://fastapi.tiangolo.com/tutorial/path-params/#__code_13
    try:
        URI = coil_uri
        if path.startswith("user/"):
            URI = coil_api_uri
        data = await request.json()
        headers = {
            "Content-Type": request.headers["Content-Type"],
            "Authorization": request.headers.get("Authorization"),
        }
        # print("____________________________________________________________________________")
        # print("POST REQUEST:", f"{URI}/{path}", headers)
        # print("____________________________________________________________________________")
        async with httpx.AsyncClient() as client:
            proxy = await client.post(f"{URI}/{path}", headers=headers, data=data)
        response = Response(content=proxy.content, status_code=proxy.status_code)
        return response
    except Exception as e:
        # print("____________________________________________________________________________")
        # print("POST ERROR:", e)
        # print("____________________________________________________________________________")
        raise HTTPException(status_code=403, detail=str(e))


@router.get("/proxy/{path:path}")
async def proxy_get_request(*, path: str, request: Request) -> Any:
    try:
        URI = coil_uri
        if path.startswith("user/"):
            URI = coil_api_uri
        headers = {
            "Content-Type": request.headers.get("Content-Type", "application/x-www-form-urlencoded"),
            "Authorization": request.headers["Authorization"],
        }
        # print("____________________________________________________________________________")
        # print("GET REQUEST:", f"{URI}/{path}", headers)
        # print("____________________________________________________________________________")
        async with httpx.AsyncClient() as client:
            proxy = await client.get(f"{URI}/{path}", headers=headers)
        # print("____________________________________________________________________________")
        # print("GET RESPONSE:", proxy.content)
        # print("____________________________________________________________________________")
        response = Response(content=proxy.content, status_code=proxy.status_code)
        return response
    except Exception as e:
        # print("____________________________________________________________________________")
        # print("GET:", e)
        # print("____________________________________________________________________________")
        raise HTTPException(status_code=403, detail=str(e))
