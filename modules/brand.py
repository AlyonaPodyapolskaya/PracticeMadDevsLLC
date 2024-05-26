from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from models.models import Brand
from models.schemas import BrandCreate, BrandResponse
from database import get_db

brands = APIRouter()

# Маршруты для сущности Brand


@brands.post("/", response_model=BrandResponse, status_code=status.HTTP_201_CREATED, summary="Создать новый бренд")
def create_brand(brand: BrandCreate, db: Session = Depends(get_db)):
    """
    Создать новый бренд.

    Параметры:
    - brand: BrandCreate - Данные для создания бренда.

    Возвращает:
    - BrandResponse: Созданный бренд.
    """
    try:
        db_brand = Brand(**brand.dict())
        db.add(db_brand)
        db.commit()
        db.refresh(db_brand)
        return db_brand
    except Exception as e:
        raise HTTPException(status_code=500, detail="Произошла ошибка при создании бренда - " + str(e))


@brands.get("/{brand_id}", response_model=BrandResponse, status_code=status.HTTP_200_OK, summary="Получить бренд по ID")
def read_brand(brand_id: int, db: Session = Depends(get_db)):
    """
    Получить бренд по ID.

    Параметры:
    - brand_id (int): ID бренда для получения.

    Возвращает:
    - BrandResponse: Полученный бренд.
    """
    try:
        db_brand = db.query(Brand).filter(Brand.id == brand_id).first()
        if db_brand is None:
            raise HTTPException(status_code=404, detail="Бренд не найден")
        return db_brand
    except Exception as e:
        raise HTTPException(status_code=500, detail="Произошла ошибка при чтении бренда - " + str(e))


@brands.put("/{brand_id}", response_model=BrandResponse, status_code=status.HTTP_200_OK, summary="Обновить бренд по ID")
def update_brand(brand_id: int, brand: BrandCreate, db: Session = Depends(get_db)):
    """
    Обновить бренд по ID.

    Параметры:
    - brand_id (int): ID бренда для обновления.
    - brand: BrandCreate - Обновленные данные бренда.

    Возвращает:
    - BrandResponse: Обновленный бренд.
    """
    try:
        db_brand = db.query(Brand).filter(Brand.id == brand_id).first()
        if db_brand is None:
            raise HTTPException(status_code=404, detail="Бренд не найден")
        for attr, value in brand.dict().items():
            setattr(db_brand, attr, value)
        db.commit()
        db.refresh(db_brand)
        return db_brand
    except Exception as e:
        raise HTTPException(status_code=500, detail="Произошла ошибка при обновлении бренда - " + str(e))


@brands.delete("/{brand_id}", response_model=BrandResponse, status_code=status.HTTP_200_OK, summary="Удалить бренд по ID")
def delete_brand(brand_id: int, db: Session = Depends(get_db)):
    """
    Удалить бренд по ID.

    Параметры:
    - brand_id (int): ID бренда для удаления.

    Возвращает:
    - BrandResponse: Удаленный бренд.
    """
    try:
        db_brand = db.query(Brand).filter(Brand.id == brand_id).first()
        if db_brand is None:
            raise HTTPException(status_code=404, detail="Бренд не найден")
        db.delete(db_brand)
        db.commit()
        return db_brand
    except Exception as e:
        raise HTTPException(status_code=500, detail="Произошла ошибка при удалении бренда - " + str(e))
