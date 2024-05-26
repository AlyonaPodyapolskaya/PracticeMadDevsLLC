from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)

    payments = relationship("Payment", back_populates="user")
    statistics = relationship("Statistic", back_populates="user")


class Store(Base):
    __tablename__ = 'stores'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

    products = relationship("Product", back_populates="store")
    payments = relationship("Payment", back_populates="store")
    statistics = relationship("Statistic", back_populates="store")


class Brand(Base):
    __tablename__ = 'brands'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

    products = relationship("Product", back_populates="brand")


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    store_id = Column(Integer, ForeignKey('stores.id'))
    brand_id = Column(Integer, ForeignKey('brands.id'))

    store = relationship("Store", back_populates="products")
    brand = relationship("Brand", back_populates="products")
    payments = relationship("Payment", back_populates="product")
    statistics = relationship("Statistic", back_populates="product")


class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    description = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    store_id = Column(Integer, ForeignKey('stores.id'))

    user = relationship("User", back_populates="payments")
    product = relationship("Product", back_populates="payments")
    store = relationship("Store", back_populates="payments")


class Statistic(Base):
    __tablename__ = 'statistics'

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, index=True)  # Тип события
    event_time = Column(DateTime, index=True, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    store_id = Column(Integer, ForeignKey('stores.id'))

    user = relationship("User", back_populates="statistics")
    product = relationship("Product", back_populates="statistics")
    store = relationship("Store", back_populates="statistics")
