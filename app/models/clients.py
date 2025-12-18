from pydantic import BaseModel

class CreateClient(BaseModel):
    name: str
    email: str
    password: str
