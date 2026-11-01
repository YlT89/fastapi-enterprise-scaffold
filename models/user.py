from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, timezone

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(min_length=3, unique=True, index=True)
    email: str = Field(index=True)
    hashed_password: str = Field(exclude=True)
    role: str = Field(default='user')
    disabled: bool = Field(default=False)
    create_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


    addresses: List['Address'] = Relationship(back_populates='user', cascade_delete=True)



from models.address import Address
User.model_rebuild()