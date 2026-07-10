from pydantic import BaseModel, Field, EmailStr


class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=100)

    email: EmailStr

    phone_number: str | None = None

    password: str = Field(min_length=6)


class RegisterResponse(BaseModel):
    id: int

    username: str

    email: EmailStr

    role: str

    message: str