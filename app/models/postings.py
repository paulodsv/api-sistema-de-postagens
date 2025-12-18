from pydantic import BaseModel
from enum import Enum

class CreatePosting(BaseModel):
    client_id: int
    description: str
    weight_kg: float
    volume_cm3: int

class PostStatus(str, Enum):
    pending = "pending"
    shipped = "shipped"
    delivered = "delivered"


