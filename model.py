from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, Date, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from typing import List, Optional
from datetime import date
from settings import DBSettings

from sqlalchemy.orm import relationship, Mapped, Session

Base = declarative_base()
if DBSettings.DB_KIND == "sqlite":
    engine = create_engine(f"sqlite:///{DBSettings.DB_NAME}.db")
else:
    uri = DBSettings.uri()
    engine = create_engine(uri, max_overflow=100, pool_timeout=100)


class Product(BaseModel):
    id: int
    name: str
    quantity: int
    price: float
    category: str

    class Config:
        from_attributes = True


class Report(BaseModel):
    id: Optional[int]
    date: date
    report: str

    class Config:
        from_attributes = True
        nullable = True


class SalesData(BaseModel):
    date: date
    products: List[Product]

    class Config:
        from_attributes = True


class Error404(BaseModel):
    code: str = 404
    description: str


class ProductModel(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String, nullable=True)
    date = Column(Date, ForeignKey("sales_data.date"), nullable=False)  # Внешний ключ

    sales_data = relationship("SalesDataModel", back_populates="products")


class SalesDataModel(Base):
    __tablename__ = "sales_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, unique=True, nullable=False)

    products: Mapped[List[ProductModel]] = relationship(
        "ProductModel", back_populates="sales_data", cascade="all, delete-orphan"
    )


class ReportModel(Base):
    __tablename__ = "report"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, unique=True, nullable=False)
    report = Column(String, nullable=False)


Base.metadata.create_all(engine)


def get_db():
    with Session(engine) as session:
        yield session
