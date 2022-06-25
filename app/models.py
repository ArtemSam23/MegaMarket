import enum

from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relation

from .database import Base


class Type(enum.Enum):
    category = "CATEGORY"
    offer = "OFFER"


class Item(Base):
    __tablename__ = "items"
    type = Column(Enum(Type))
    name = Column(String, index=True)
    id = Column(String, primary_key=True)
    price = Column(Integer, nullable=True)
    parentId = Column(String, ForeignKey("items.id"), nullable=True)
    date = Column(DateTime(timezone=True))
    children = relation('Item', remote_side=[parentId], cascade="all,delete")
