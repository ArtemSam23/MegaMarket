import datetime

from fastapi import Depends, FastAPI, Path
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from . import crud, models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)


responses = {
    "200": {"description": "Success"},
    "400": {"description": "Item not found"},
    "404": {"description": "Validation failed"},
    "422": {"description": "Is not returned by the server"}
    # 422 статус код нельзя убрать из openapi.yaml, потому что он дефолтный для FastAPI
    # Сервис его не возвращает, поэтому просто переопределим его описание для схемы
}

app = FastAPI(responses=responses)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    )


# Изменяем изначальный 422 статус FastApi на 400 и добавляем модель, которая не прошла валидацию
# noinspection PyUnusedLocal
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"code": 400, "message": "Validation Failed"})
        # content=jsonable_encoder({"detail": exc.errors(), "body": exc.body})
    )


# Плохой тон и так делать нельзя!
# Используется для обработки ошибок базы данных, если они произошли в crud.py и не были обработаны
# noinspection PyUnusedLocal
@app.exception_handler(500)
async def internal_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"code": 400, "message": "Validation Failed"})
    )


@app.post("/imports", response_model=schemas.Item)
async def create_items(data: schemas.ItemImport, db: Session = Depends(get_db)):
    """
    Импорт новых товаров или категорий. Товары/категории импортированные повторно обновляются.
    """
    try:
        crud.create_items(db, data.items)
    except crud.ParentNotFound as exc:
        raise RequestValidationError({"message": str(exc)})


@app.get("/nodes/{id}", response_model=schemas.Item)
async def get_item(item_id: str = Path(..., alias='id'), db: Session = Depends(get_db)):
    """
    Получение товара/категории по id.
    """
    db_item = crud.get_item(db, item_id)
    if db_item:
        return db_item
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=jsonable_encoder({"code": 404, "message": "Item not found"}),
    )


@app.delete("/delete/{id}")
async def delete_item(item_id: str = Path(..., alias='id'), db: Session = Depends(get_db)):
    """
    Удаление товара/категории по id. При удалении категории все ее дочерние товары/категории удаляются.
    """
    db_item = crud.get_item(db, item_id)
    if db_item:
        crud.delete_item(db, db_item)
        return JSONResponse(status_code=status.HTTP_200_OK, content=None)
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=jsonable_encoder({"code": 404, "message": "Item not found"}),
    )


@app.get("/sales", response_model=list[schemas.Item])
async def get_sales(date: datetime.datetime, db: Session = Depends(get_db)):
    """
    Получение списка товаров, проданных за период [date - 1 day, date].
    """
    current_time = date
    one_day_ago = current_time - datetime.timedelta(hours=24)
    return crud.get_sales(db, one_day_ago, current_time)
