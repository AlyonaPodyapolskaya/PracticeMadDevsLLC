import uvicorn
from fastapi import FastAPI
from database import init_db, create_tables
from modules.brand import brands
from modules.payment import payments
from modules.shop import stores
from modules.statistic import statistics
from modules.user import users
from modules.product import products

app = FastAPI(docs_url="/")


app.include_router(statistics, tags=["Статистика"], prefix="/statistics")
app.include_router(brands, tags=["Бренды"], prefix="/brands")
app.include_router(stores, tags=["Магазины"], prefix="/stores")
app.include_router(users, tags=["Пользователи"], prefix="/users")
app.include_router(products, tags=["Продукты"], prefix="/products")
app.include_router(payments, tags=["Платежи"], prefix="/payments")


if __name__ == "__main__":
    init_db()
    create_tables()
    uvicorn.run(app, host="127.0.0.1", port=8000)
