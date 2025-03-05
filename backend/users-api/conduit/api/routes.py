from fastapi import APIRouter

from conduit.api.users.get_current_user.endpoint import router as get_current_user
from conduit.api.users.login_user.endpoint import router as login_user
from conduit.api.users.register_user.endpoint import router as register_user
from conduit.api.users.update_current_user.endpoint import router as update_current_user

router = APIRouter(prefix="/api")

router.include_router(register_user)
router.include_router(login_user)
router.include_router(get_current_user)
router.include_router(update_current_user)
