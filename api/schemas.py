from typing import Optional, Union
from pydantic import BaseModel, root_validator, validator
from pydantic.schema import datetime

from .models import Type


def explore_category(children):
    sum_price = 0
    count_offers = 0

    for child in children:
        if child.type == Type.offer:
            sum_price += child.price
            count_offers += 1
        else:
            s, c = explore_category(child.children)
            sum_price += s
            count_offers += c

    return sum_price, count_offers


class Item(BaseModel):
    type: Type
    id: str
    name: str
    price: Union[int, None]
    parentId: Optional[str]
    date: datetime
    children: Optional[list["Item"]]

    @root_validator()
    def set_price(cls, values):
        if values["type"] == Type.category:
            children = values.get("children")
            if children:
                sum_offers, count_offers = explore_category(children)
                if count_offers == 0:
                    values["price"] = None
                else:
                    values["price"] = sum_offers//count_offers
        else:
            values["children"] = None
        return values

    class Config:
        orm_mode = True


class ItemCreate(BaseModel):
    type: Type
    id: str
    name: str
    price: Union[int, None]
    parentId: Optional[str]
    date: Optional[datetime]

    @validator('price')
    def validate_price(cls, price, values):
        if values["type"] == Type.category:
            if price is not None:
                raise TypeError('Validation Failed')
        elif type(price) is int:
            raise TypeError('Validation Failed')

    class Config:
        orm_mode = True
