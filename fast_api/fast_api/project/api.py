from project.app import app
from utils.pydantic.response.responses import SuccessResponse


@app.get("/ping", tags=["ping"])
async def ping():
    return SuccessResponse(data="ok")
