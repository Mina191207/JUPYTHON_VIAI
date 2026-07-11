from pydantic import BaseModel, Field, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    email: EmailStr

    first_name: str | None = Field(max_length=100)

    last_name: str | None = Field(max_length=100)

    phone_number: str | None = None

    password: str = Field(min_length=6)


class RegisterResponse(BaseModel):
    id: int

    email: EmailStr

    first_name: str | None = None

    last_name: str | None = None

    role: str

    message: str