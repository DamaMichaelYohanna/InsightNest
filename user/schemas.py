from sqlmodel import SQLModel


class LoginSchema(SQLModel):
    """Schema to be used for login"""
    username: str
    password: str


class LoginFailedSchema(SQLModel):
    detail: str


class LoginReturnSchema(SQLModel):
    id: int
    username: str
    full_name: str | None = None
    error: LoginFailedSchema = None


class RegisterInSchema(SQLModel):
    """Schema for receiving user credentials"""
    username: str
    email: str | None = None
    password: str


class RegisterOutSchema(SQLModel):
    """Schema to output user info after registration"""
    id: int
    username: str
    email: str | None = None
