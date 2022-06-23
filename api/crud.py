from sqlalchemy.orm import Session


from . import models, schemas


def get_item(db: Session, item_id):
    return db.query(models.Item).get(item_id)


def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_parents_date(db: Session, parent_id, date):
    db_parent: models.Item = db.query(models.Item).get(parent_id)
    db_parent.date = date
    db.commit()


def update_item(db: Session, item: schemas.ItemCreate):
    db_item: models.Item = db.query(models.Item).get(item.id)
    db_item.name = item.name
    db_item.price = item.price
    db_item.parentId = item.parentId
    print(db_item.parentId)
    db_item.date = item.date
    db.commit()
    db.refresh(db_item)
    return db_item


def get_items(db: Session):
    return db.query(models.Item).all()


def get_tree(db: Session):
    return db.query(models.Item).filter(models.Item.parentId == None).all()


def create_item_with_children(db: Session, item: schemas.ItemCreate):
    """Функция создания Item с детьми"""
    db_item = models.Item(**item.dict(exclude={'children'}))
    db.add(db_item)
    if item.children:
        for child in item.children:
            create_item_with_children(db, child)
    db.commit()
    db.refresh(db_item)
    return db_item
