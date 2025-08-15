from pydantic import BaseModel


class UserInput(BaseModel):
    username: str = ""
    email: str = ""
    phone: str = ""
    password: str = ""

class UserLoginInput(UserInput):
    stay_login: bool = False

class UserPasswordResetInput(UserInput):
    uid: str = ""

class UserVerificationCreateInput(BaseModel):
    email: str = ""
    phone: str = ""

class UserVerificationInput(UserVerificationCreateInput):
    code: str = ""

