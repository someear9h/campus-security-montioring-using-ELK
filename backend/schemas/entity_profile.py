from pydantic import BaseModel, EmailStr
from typing import Optional

class EntityProfile(BaseModel):
    """
    Represents the complete, resolved profile of a campus entity.
    This model validates the data retrieved from the 'entities' index.
    Optional fields handle cases where a student is not staff and vice-versa.
    """
    entity_id: str
    name: str
    role: str
    email: EmailStr
    department: str
    student_id: Optional[str] = None
    staff_id: Optional[str] = None
    card_id: Optional[str] = None
    device_hash: Optional[str] = None
    face_id: Optional[str] = None

    class Config:
        # This allows the model to be created from ORM objects,
        # which is good practice.
        orm_mode = True
