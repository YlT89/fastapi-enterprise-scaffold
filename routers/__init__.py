from fastapi import APIRouter
from .user_routers  import user_router
from .order_routers import order_router
from .auth_routers import auth_router


api_v2 = APIRouter(prefix='/api')
api_v2.include_router(auth_router)
api_v2.include_router(user_router)
api_v2.include_router(order_router)