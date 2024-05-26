from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from models.models import Store
from models.schemas import StoreCreate, StoreResponse
from database import get_db

stores = APIRouter()

# Маршруты для сущности Store


@stores.post("/", response_model=StoreResponse, status_code=status.HTTP_201_CREATED, summary="Создать новый магазин")
def create_store(store: StoreCreate, db: Session = Depends(get_db)):
    """
    Создать новый магазин.

    Параметры:
    - store: StoreCreate - Данные для создания магазина.

    Возвращает:
    - StoreResponse: Созданный магазин.
    """
    try:
        db_store = Store(**store.dict())
        db.add(db_store)
        db.commit()
        db.refresh(db_store)
        return db_store
    except Exception as e:
        raise HTTPException(status_code=500, detail="Произошла ошибка при создании магазина - " + str(e))


@stores.get("/{store_id}", response_model=StoreResponse, status_code=status.HTTP_200_OK, summary="Получить магазин по ID")
def read_store(store_id: int, db: Session = Depends(get_db)):
    """
    Получить магазин по ID.

    Параметры:
    - store_id (int): ID магазина для получения.

    Возвращает:
    - StoreResponse: Полученный магазин.
    """
    try:
        db_store = db.query(Store).filter(Store.id == store_id).first()
        if db_store is None:
            raise HTTPException(status_code=404, detail="Магазин не найден")
        return db_store
    except Exception as e:
        raise HTTPException(status_code=500, detail="Произошла ошибка при чтении магазина - " + str(e))


@stores.put("/{store_id}", response_model=StoreResponse, status_code=status.HTTP_200_OK, summary="Обновить магазин по ID")
def update_store(store_id: int, store: StoreCreate, db: Session = Depends(get_db)):
    """
    Обновить магазин по ID.

    Параметры:
    - store_id (int): ID магазина для обновления.
    - store: StoreCreate - Обновленные данные магазина.

    Возвращает:
    - StoreResponse: Обновленный магазин.
    """
    try:
        db_store = db.query(Store).filter(Store.id == store_id).first()
        if db_store is None:
            raise HTTPException(status_code=404, detail="Магазин не найден")
        for attr, value in store.dict().items():
            setattr(db_store, attr, value)
        db.commit()
        db.refresh(db_store)
        return db_store
    except Exception as e:
        raise HTTPException(status_code=500, detail="Произошла ошибка при обновлении магазина - " + str(e))


@stores.delete("/{store_id}", response_model=StoreResponse, status_code=status.HTTP_200_OK, summary="Удалить магазин по ID")
def delete_store(store_id: int, db: Session = Depends(get_db)):
    """
    Удалить магазин по ID.

    Параметры:
    - store_id (int): ID магазина для удаления.

    Возвращает:
    - StoreResponse: Удаленный магазин.
    """
    try:
        db_store = db.query(Store).filter(Store.id == store_id).first()
        if db_store is None:
            raise HTTPException(status_code=404, detail="Магазин не найден")
        db.delete(db_store)
        db.commit()
        return db_store
    except Exception as e:
        raise HTTPException(status_code=500, detail="Произошла ошибка при удалении магазина - " + str(e))
