from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from models.models import Product
from models.schemas import ProductCreate, ProductResponse
from database import get_db

products = APIRouter()

# Маршруты для сущности Product


@products.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED, summary="Создать новый продукт")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """
    Создать новый продукт.

    Параметры:
    - product: ProductCreate - Данные для создания продукта.

    Возвращает:
    - ProductResponse: Созданный продукт.
    """
    try:
        db_product = Product(**product.dict())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except Exception as e:
        raise HTTPException(status_code=500, detail="Произошла ошибка при создании продукта - " + str(e))


@products.get("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK, summary="Получить продукт по ID")
def read_product(product_id: int, db: Session = Depends(get_db)):
    """
    Получить продукт по ID.

    Параметры:
    - product_id (int): ID продукта для получения.

    Возвращает:
    - ProductResponse: Полученный продукт.
    """
    try:
        db_product = db.query(Product).filter(Product.id == product_id).first()
        if db_product is None:
            raise HTTPException(status_code=404, detail="Продукт не найден")
        return db_product
    except Exception as e:
        raise HTTPException(status_code=500, detail="Произошла ошибка при чтении продукта - " + str(e))


@products.put("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK, summary="Обновить продукт по ID")
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    """
    Обновить продукт по ID.

    Параметры:
    - product_id (int): ID продукта для обновления.
    - product: ProductCreate - Обновленные данные продукта.

    Возвращает:
    - ProductResponse: Обновленный продукт.
    """
    try:
        db_product = db.query(Product).filter(Product.id == product_id).first()
        if db_product is None:
            raise HTTPException(status_code=404, detail="Продукт не найден")
        for attr, value in product.dict().items():
            setattr(db_product, attr, value)
        db.commit()
        db.refresh(db_product)
        return db_product
    except Exception as e:
        raise HTTPException(status_code=500, detail="Произошла ошибка при обновлении продукта - " + str(e))


@products.delete("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK, summary="Удалить продукт по ID")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Удалить продукт по ID.

    Параметры:
    - product_id (int): ID продукта для удаления.

    Возвращает:
    - ProductResponse: Удаленный продукт.
    """
    try:
        db_product = db.query(Product).filter(Product.id == product_id).first()
        if db_product is None:
            raise HTTPException(status_code=404, detail="Продукт не найден")
        db.delete(db_product)
        db.commit()
        return db_product
    except Exception as e:
        raise HTTPException(status_code=500, detail="Произошла ошибка при удалении продукта - " + str(e))
