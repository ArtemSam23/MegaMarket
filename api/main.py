from fastapi import Depends, FastAPI, Path
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


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
def create_items(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, item=item)
