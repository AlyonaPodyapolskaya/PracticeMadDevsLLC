from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./shops.db"

# Создание синхронного соединения с базой данных
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Определение синхронной сессии для работы с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Функция для инициализации базы данных
def init_db():
    Base.metadata.create_all(bind=engine)


# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Функция для создания таблиц
def create_tables():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
