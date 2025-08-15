from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from project.app import app


@app.exception_handler(Exception)
async def exception_handler(request, exc):
    return JSONResponse(
        content=jsonable_encoder({"message": str(exc)}),
    )