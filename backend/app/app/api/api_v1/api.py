from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    login,
    users,
    creators,
    works,
    contracts,
    utils,
    sources,
    search,
    stream,
    pay_stripe,
    pay_coil,
    proxy,
)

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(creators.router, prefix="/creators", tags=["creators"])
api_router.include_router(works.router, prefix="/works", tags=["works"])
api_router.include_router(contracts.router, prefix="/contracts", tags=["contracts"])
api_router.include_router(sources.router, prefix="/sources", tags=["sources"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(stream.router, prefix="/stream", tags=["stream"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(pay_stripe.router, prefix="/stripe", tags=["stripe"])
api_router.include_router(pay_coil.router, prefix="/coil", tags=["coil"])
api_router.include_router(proxy.router, prefix="/proxy", tags=["proxy"])
