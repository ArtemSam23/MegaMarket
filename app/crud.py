from datetime import datetime

from sqlalchemy import and_
from sqlalchemy.orm import Session

from . import models, schemas


class ParentNotFound(Exception):
    pass


def get_item(db: Session, item_id):
    return db.query(models.Item).get(item_id)


def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    if db_item.parentId:
        update_parents_date(db, db_item.parentId, item.date)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_items(db: Session, items: list[schemas.ItemCreate]):
    for item in items:
        if get_item(db, item.id):
            update_item(db, item)
        else:
            create_item(db, item)


def delete_item(db: Session, db_item):
    db.delete(db_item)
    db.commit()


def update_parents_date(db: Session, parent_id, date):
    db_parent: models.Item = db.query(models.Item).get(parent_id)
    if db_parent:
        db_parent.date = date
        if db_parent.parentId:
            update_parents_date(db, db_parent.parentId, date)
        db.commit()
    else:
        raise ParentNotFound(f"Parent with id {parent_id} not found")


def update_item(db: Session, item: schemas.ItemCreate):
    db_item: models.Item = db.query(models.Item).get(item.id)
    db_item.name = item.name
    db_item.price = item.price
    db_item.parentId = item.parentId
    db_item.date = item.date
    if db_item.parentId:
        update_parents_date(db, db_item.parentId, item.date)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_sales(db: Session, date_start: datetime, date_end: datetime):
    db_sales = db.query(models.Item).filter(
        and_(
            models.Item.type == models.Type.offer,
            date_start <= models.Item.date,
            models.Item.date <= date_end)
    ).all()
    return db_sales
