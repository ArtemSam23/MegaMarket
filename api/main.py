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


# Изменяем изначальный 422 статус FastApi на 400 и добавляем модель, которая не прошла валидацию
# noinspection PyUnusedLocal
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        # content=jsonable_encoder({"message": "Validation Failed"})
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body})
    )


# Сессия базы данных
# Для каждого запроса будет использоваться отдельная сессия
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/imports", response_model=schemas.Item)
def create_items(data: schemas.ItemImport, db: Session = Depends(get_db)):
    crud.create_items(db, data.items)


@app.get("/nodes/{id}", response_model=schemas.Item)
def get_item(item_id: str = Path(..., alias='id'), db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id)
    if db_item:
        return db_item
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=jsonable_encoder({"message": "Item not found"}),
    )


@app.delete("/delete/{id}")
def delete_item(item_id: str = Path(..., alias='id'), db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id)
    if db_item:
        crud.delete_item(db, db_item)
        return JSONResponse(status_code=status.HTTP_200_OK, content=None)
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=jsonable_encoder({"message": "Item not found"}),
    )
