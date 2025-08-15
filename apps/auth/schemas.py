from pydantic import BaseModel,field_validator


class UserListInput(BaseModel):
    age: int = 19
    name: str = "子健"
    email: str = "表哥@.com"

    @field_validator("age",mode="before")
    @classmethod
    def validate_age(cls, age):
        print(f"age:{age}")
        if 0 <= age <= 18:
            return 2
        else:
            raise ValueError("age must be between 0 and 18")

