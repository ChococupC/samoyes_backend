from pydantic import BaseModel, field_validator


class UserListInput(BaseModel):
    limit: int = 10
    offset: int = 0
    age: int = 19
    name: str = "子健"
    emai: str = "表哥@.com"

    @field_validator("age", mode="before")
    @classmethod
    def validator_age(cls, age: int):
        print(f"age:{age}")
        if 0 <= age <= 18:
            return age
        else:
            raise ValueError("age must be between 0 and 18")
