from pydantic import BaseModel


class ResponseModel(BaseModel):
    code: int = 200
    message: str = "success"
    data: dict = {}
    status: str = "success"


class ListResponseModel(ResponseModel):
    limit: int = 10
    offset: int = 0
    total: int = 0


class SuccessResponseModel(ResponseModel):
    code: int = 200


class ErrorResponseModel(BaseModel):
    code: int = 400
    message: str = "error"
    data: dict = {}
    status: str = "error"


class LoginErrorResponse(ErrorResponseModel):
    code: int = 401
    message: str = "login error"
