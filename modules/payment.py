from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from models.models import Payment
from models.schemas import PaymentCreate, PaymentResponse
from database import get_db

payments = APIRouter()

# Маршруты для сущности Payment


@payments.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED, summary="Создать новый платеж")
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    """
    Создать новый платеж.

    Параметры:
    - payment: PaymentCreate - Данные для создания платежа.

    Возвращает:
    - PaymentResponse: Созданный платеж.
    """
    try:
        db_payment = Payment(**payment.dict())
        db.add(db_payment)
        db.commit()
        db.refresh(db_payment)
        return db_payment
    except Exception as e:
        raise HTTPException(status_code=500, detail="Произошла ошибка при создании платежа - " + str(e))


@payments.get("/{payment_id}", response_model=PaymentResponse, status_code=status.HTTP_200_OK, summary="Получить платеж по ID")
def read_payment(payment_id: int, db: Session = Depends(get_db)):
    """
    Получить платеж по ID.

    Параметры:
    - payment_id (int): ID платежа для получения.

    Возвращает:
    - PaymentResponse: Полученный платеж.
    """
    try:
        db_payment = db.query(Payment).filter(Payment.id == payment_id).first()
        if db_payment is None:
            raise HTTPException(status_code=404, detail="Платеж не найден")
        return db_payment
    except Exception as e:
        raise HTTPException(status_code=500, detail="Произошла ошибка при чтении платежа - " + str(e))


@payments.put("/{payment_id}", response_model=PaymentResponse, status_code=status.HTTP_200_OK, summary="Обновить платеж по ID")
def update_payment(payment_id: int, payment: PaymentCreate, db: Session = Depends(get_db)):
    """
    Обновить платеж по ID.

    Параметры:
    - payment_id (int): ID платежа для обновления.
    - payment: PaymentCreate - Обновленные данные платежа.

    Возвращает:
    - PaymentResponse: Обновленный платеж.
    """
    try:
        db_payment = db.query(Payment).filter(Payment.id == payment_id).first()
        if db_payment is None:
            raise HTTPException(status_code=404, detail="Платеж не найден")
        for attr, value in payment.dict().items():
            setattr(db_payment, attr, value)
        db.commit()
        db.refresh(db_payment)
        return db_payment
    except Exception as e:
        raise HTTPException(status_code=500, detail="Произошла ошибка при обновлении платежа - " + str(e))


@payments.delete("/{payment_id}", response_model=PaymentResponse, status_code=status.HTTP_200_OK, summary="Удалить платеж по ID")
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    """
    Удалить платеж по ID.

    Параметры:
    - payment_id (int): ID платежа для удаления.

    Возвращает:
    - PaymentResponse: Удаленный платеж.
    """
    try:
        db_payment = db.query(Payment).filter(Payment.id == payment_id).first()
        if db_payment is None:
            raise HTTPException(status_code=404, detail="Платеж не найден")
        db.delete(db_payment)
        db.commit()
        return db_payment
    except Exception as e:
        raise HTTPException(status_code=500, detail="Произошла ошибка при удалении платежа - " + str(e))
