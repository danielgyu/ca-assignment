from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: int
    password: str


class RegisterUserRequest(BaseModel):
    username: str
    password: str

    def check_password_constraint(self) -> bool:
        return True if len(self.password) > 8 else False


class RegisterUserResponse(BaseModel):
    success: bool
    reason: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    success: bool
    token: str
