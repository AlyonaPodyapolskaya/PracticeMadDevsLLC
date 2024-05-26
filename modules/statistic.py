from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from models.models import Statistic
from models.schemas import StatisticCreate, StatisticResponse
from database import get_db

statistics = APIRouter()

# Маршруты для сущности Statistic


@statistics.post("/", response_model=StatisticResponse, status_code=status.HTTP_201_CREATED, summary="Создать новую статистику")
def create_statistic(statistic: StatisticCreate, db: Session = Depends(get_db)):
    """
    Создать новую статистику.

    Параметры:
    - statistic: StatisticCreate - Данные для создания статистики.

    Возвращает:
    - StatisticResponse: Созданная статистика.
    """
    try:
        db_statistic = Statistic(**statistic.dict())
        db.add(db_statistic)
        db.commit()
        db.refresh(db_statistic)
        return db_statistic
    except Exception as e:
        raise HTTPException(status_code=500, detail="Произошла ошибка при создании статистики - " + str(e))


@statistics.get("/{statistic_id}", response_model=StatisticResponse, status_code=status.HTTP_200_OK, summary="Получить статистику по ID")
def read_statistic(statistic_id: int, db: Session = Depends(get_db)):
    """
    Получить статистику по ID.

    Параметры:
    - statistic_id (int): ID статистики для получения.

    Возвращает:
    - StatisticResponse: Полученная статистика.
    """
    try:
        db_statistic = db.query(Statistic).filter(Statistic.id == statistic_id).first()
        if db_statistic is None:
            raise HTTPException(status_code=404, detail="Статистика не найдена")
        return db_statistic
    except Exception as e:
        raise HTTPException(status_code=500, detail="Произошла ошибка при чтении статистики - " + str(e))


@statistics.put("/{statistic_id}", response_model=StatisticResponse, status_code=status.HTTP_200_OK, summary="Обновить статистику по ID")
def update_statistic(statistic_id: int, statistic: StatisticCreate, db: Session = Depends(get_db)):
    """
    Обновить статистику по ID.

    Параметры:
    - statistic_id (int): ID статистики для обновления.
    - statistic: StatisticCreate - Обновленные данные статистики.

    Возвращает:
    - StatisticResponse: Обновленная статистика.
    """
    try:
        db_statistic = db.query(Statistic).filter(Statistic.id == statistic_id).first()
        if db_statistic is None:
            raise HTTPException(status_code=404, detail="Статистика не найдена")
        for attr, value in statistic.dict().items():
            setattr(db_statistic, attr, value)
        db.commit()
        db.refresh(db_statistic)
        return db_statistic
    except Exception as e:
        raise HTTPException(status_code=500, detail="Произошла ошибка при обновлении статистики - " + str(e))


@statistics.delete("/{statistic_id}", response_model=StatisticResponse, status_code=status.HTTP_200_OK, summary="Удалить статистику по ID")
def delete_statistic(statistic_id: int, db: Session = Depends(get_db)):
    """
    Удалить статистику по ID.

    Параметры:
    - statistic_id (int): ID статистики для удаления.

    Возвращает:
    - StatisticResponse: Удаленная статистика.
    """
    try:
        db_statistic = db.query(Statistic).filter(Statistic.id == statistic_id).first()
        if db_statistic is None:
            raise HTTPException(status_code=404, detail="Статистика не найдена")
        db.delete(db_statistic)
        db.commit()
        return db_statistic
    except Exception as e:
        raise HTTPException(status_code=500, detail="Произошла ошибка при удалении статистики - " + str(e))
