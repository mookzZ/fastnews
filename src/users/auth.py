from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from fastapi_users import FastAPIUsers

from fastapi import Request

from src.users.manager import get_user_manager
from src.users.models import User

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

SECRET = "awzsxedcrfvtgbyhunjmikolp"

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

async def get_enabled_backends(request: Request):
    return [auth_backend]

current_active_user = fastapi_users.current_user(active=True, get_enabled_backends=get_enabled_backends)