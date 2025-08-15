from project.app import app
from utils.pydantic_utils.response import SuccessResponseModel


@app.get("/ping", tags=["ping"])
async def ping():
    return SuccessResponseModel(data="ok")
