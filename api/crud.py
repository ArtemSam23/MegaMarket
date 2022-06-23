from sqlalchemy import null
from sqlalchemy.orm import Session


from . import models, schemas


def get_items(db: Session):
    return db.query(models.Item).all()


def get_item(db: Session, item_id):
    return db.query(models.Item).get(item_id)


def get_tree(db: Session):
    return db.query(models.Item).filter(models.Item.type == models.Type.category and models.Item.parentId == null).all()


def create_or_update_item(db: Session, item: schemas.Item):
    db_item = models.Item(**item.dict(exclude={'children'}))
    if item.children:
        for child in item.children:
            create_or_update_item(db, child)
    db.commit()
    db.refresh(db_item)
    return db_item
