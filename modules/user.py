from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from models.schemas import UserCreate, UserResponse
from database import get_db
from models.models import User

users = APIRouter()

# Маршруты для сущности User


@users.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Создать пользователя")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Создать нового пользователя.

    Параметры:
    - user: UserCreate - Данные для создания пользователя.

    Возвращает:
    - UserResponse: Созданный пользователь.
    """
    try:
        # Проверка уникальности имени пользователя
        existing_user = db.query(User).filter(User.username == user.username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Имя пользователя уже занято")

        db_user = User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail="Произошла ошибка при создании пользователя -  " + str(e))


@users.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK, summary="Получить пользователя по ID")
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Получить пользователя по ID.

    Параметры:
    - user_id (int): ID пользователя для получения.

    Возвращает:
    - UserResponse: Полученный пользователь.
    """
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail="Произошла ошибка при чтении пользователя - " + str(e))


@users.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK, summary="Обновить пользователя по ID")
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    """
    Обновить пользователя по ID.

    Параметры:
    - user_id (int): ID пользователя для обновления.
    - user: UserCreate - Обновленные данные пользователя.

    Возвращает:
    - UserResponse: Обновленный пользователь.
    """
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        for attr, value in user.dict().items():
            setattr(db_user, attr, value)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail="Произошла ошибка при обновлении пользователя - " + str(e))


@users.delete("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK, summary="Удалить пользователя по ID")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Удалить пользователя по ID.

    Параметры:
    - user_id (int): ID пользователя для удаления.

    Возвращает:
    - UserResponse: Удаленный пользователь.
    """
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        db.delete(db_user)
        db.commit()
        return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail="Произошла ошибка при удалении пользователя - " + str(e))
