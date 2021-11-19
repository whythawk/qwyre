from fastapi import APIRouter

from app.api.api_v1.endpoints import login, users, utils, epub, pay_stripe, pay_coil

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(epub.router, prefix="/chapisha", tags=["chapisha"])
api_router.include_router(pay_stripe.router, prefix="/stripe", tags=["stripe"])
api_router.include_router(pay_coil.router, prefix="/coil", tags=["coil"])
