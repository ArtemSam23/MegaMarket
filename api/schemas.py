from typing import Optional

from pydantic import BaseModel
from pydantic.schema import datetime

from .models import Type


class Item(BaseModel):
    type: Type
    id: str
    name: str
    price: int
    parentId: Optional[str]
    date: datetime
    children: Optional[list["Item"]]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
