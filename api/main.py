from fastapi import Depends, FastAPI, Path
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/items/", response_model=list[schemas.Item])
def get_items(db: Session = Depends(get_db)):
    return crud.get_tree(db)


@app.get("/items/{id}", response_model=schemas.Item)
def get_item(item_id: str = Path(..., alias='id'), db: Session = Depends(get_db)):
    return crud.get_item(db, item_id)


@app.post("/items/", response_model=schemas.Item)
def create_items(item: schemas.Item, db: Session = Depends(get_db)):
    return crud.create_or_update_item(db, item=item)
