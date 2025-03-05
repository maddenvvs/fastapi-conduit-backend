from fastapi import APIRouter

from conduit.api.users.get_current_user.endpoint import router as get_current_user
from conduit.api.users.register_user.endpoint import router as register_user

router = APIRouter(prefix="/api")

router.include_router(get_current_user)
router.include_router(register_user)
