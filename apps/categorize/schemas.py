from pydantic import BaseModel


class CategorizeInput(BaseModel):
    date: str = ""