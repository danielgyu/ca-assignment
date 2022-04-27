import bcrypt
import jwt
from fastapi import APIRouter, Depends, Response, status 

from cookapps.database import get_db_connection
from cookapps.user_repository import UserRepository
from cookapps.models import (
    RegisterUserRequest,
    RegisterUserResponse,
    LoginRequest,
    LoginResponse,
)


SECRET_KEY = "secret"
router = APIRouter(prefix = "/users")


def make_token(user_id: int) -> str:
    encoded = jwt.encode(
        dict(sub=user_id),
        SECRET_KEY,
        algorithm="HS256",
    )
    return encoded


@router.post("/register")
async def user_register(
    body: RegisterUserRequest,
    response: Response,
    user_repository: UserRepository = Depends(UserRepository),
    connection = Depends(get_db_connection),
) -> RegisterUserResponse:
    if not body.check_password_constraint():
        return RegisterUserResponse(
            success=False, reason="Invalid password"
        )

    if not await user_repository.is_unique(connection, body.username):
        return RegisterUserResponse(
            success=False, reason="Username already exists"
        )

    hashed = bcrypt.hashpw(body.password.encode(), bcrypt.gensalt())
    if not await user_repository.save_user(
        connection, body.username, hashed.decode()
    ):
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return RegisterUserResponse(
            success=False, reason="Server Error"
        )

    connection.close()
    return RegisterUserResponse(success=True)


@router.post("/login")
async def user_login(
    body: LoginRequest,
    response: Response,
    user_repository: UserRepository = Depends(UserRepository),
    connection = Depends(get_db_connection),
) -> LoginResponse:
    user = await user_repository.get_user(connection, body.username)
    connection.close()
    if not user:
        response.status_code = 401
        return LoginResponse(success=False, token="")

    if not bcrypt.checkpw(
        body.password.encode(), user.password.encode()
    ):
        response.status_code = 401
        return LoginResponse(success=False, token="")

    token = make_token(user.id)
    return LoginResponse(success=True, token=token)
