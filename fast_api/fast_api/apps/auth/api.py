from fastapi import APIRouter, Depends

from apps.auth.schemas import UserListInput
from utils.pydantic.response.response import ListResponseModel, SuccessResponseModel

router = APIRouter(tags=["auth"], prefix="/auth")


@router.get("/list")
async def user_list(
        param: UserListInput = Depends(),
):
    print(param)
    return ListResponseModel()


@router.post("/{pk}")
async def user_detail(pk: int):
    # 查询数据库
    data = {
        "id": pk,
        "username": "admin",
        "email": "admin@example.com",
        "mobile": "13800138000",
        "status": 1,
        "created_at": "2021-01-01 00:00:00",
        "updated_at": "2021-01-01 00:00:00"
    }
    print(f"pd:{pk}")
    return SuccessResponseModel(data=data)


def return_data(code=200, message="success", data={}, status="success"):
    return {
        "code": code,
        "message": message,
        "data": data,
        "status": status
    }
