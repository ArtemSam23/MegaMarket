import datetime
import uuid
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
    id = Column(String, primary_key=True, default=uuid.uuid4)
    price = Column(Integer)
    parentId = Column(String, ForeignKey("items.id"), nullable=True)
    date = Column(DateTime(timezone=True), default=datetime.datetime.now().isoformat())
    children = relation('Item', remote_side=[parentId])
