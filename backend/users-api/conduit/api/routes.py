from fastapi import APIRouter

from conduit.api.users.get_current_user.endpoint import router as get_current_user

router = APIRouter(prefix="/api")

router.include_router(get_current_user)
