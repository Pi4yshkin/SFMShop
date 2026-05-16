from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, EmailStr
import redis
import json
from typing import Optional
from src.services.cache_invalidation import invalidate_cache
from src.database.connection import get_session
from src.database.models import Product as ProductModel
from contextlib import contextmanager


class CacheService:
    """Класс получения данных из кеша и кеширования"""
    def __init__(self, host='localhost', port=6379, db=0):
        try:
            self.redis_client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
            self.redis_client.ping()
            print(f"Redis запущен")
        except redis.ConnectionError:
            print(f"Нет подключения к Redis")
            self.redis_client = None

    def get_products(self)-> Optional[list]:  # Optional[list] значит, что функция должна вернуть лист, но не обязана, может вернуть None
        """Функция вывода кешированных данных из таблицы products"""
        if not self.redis_client:
            return None
        cached = self.redis_client.get('products:all')
        if cached:
            return json.loads(cached)
        return None
    
    def set_products(self, products: list, ttl: int=3600):
        """Функция кеширования данных из таблицы products"""
        if not self.redis_client:
            print(f"Redis недоступен")
            return
        self.redis_client.setex('products:all', ttl, json.dumps(products))

    def get_product(self, product_id: int)-> Optional[dict]:
        """Функция вывода продукта по его id из кеша (таблица products)"""
        if not self.redis_client:
            return None
        cached = self.redis_client.get(f'product:{product_id}')
        if cached:
            return json.loads(cached)
        return None
    
    def set_product(self, product_id, product: dict, ttl: int=3600):
        """Функция кеширования данных из таблицы products"""
        if not self.redis_client:
            print(f"Redis недоступен")
            return
        self.redis_client.setex(f'product:{product_id}', ttl, json.dumps(product))
    


app = FastAPI()

cached_service = CacheService()

class OrderCreate(BaseModel):
    user_id: int
    total: float
    status: str

class CreateOrderItems(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    price: float

class CreateUser(BaseModel):
    name: str
    email: EmailStr
    balance: float

class AddProduct(BaseModel):
    name: str
    price: float
    stock: int

class ProductPatch(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None

# uvicorn src.api.main:app --reload

def get_read_db():
    with get_session(read_only=True) as db:
        yield db

def get_write_db():
    with get_session(read_only=False) as db:
        yield db


@app.get('/products/')  # обращение к БД через FastAPI запрос

def get_products(db = Depends(get_read_db))-> Optional[list]:  # Depends позволяет выносить повторяющуюся логику из эндпоинтов и автоматически подставлять нужные значения.
    cached_products = cached_service.get_products()  # проверка есть ли данные в кеш

    if cached_products:
        print(f"Получаю данные из кеша")
        return cached_products  # вывожу если есть
    
    print(f"Кеш пуст, обращаюсь к БД")
    products = db.query(ProductModel).all()  # если нет, обращаюсь к БД

    product_data = [
        {"id": product.id, "name": product.name, "price": float(product.price), "stock": product.stock} for product in products
    ]  # собираю все в список

    print(f"Добавляю данные в кеш")
    cached_service.set_products(product_data)  # кеширую

    print(f"Возвращаю данные")
    return product_data 


@app.get("/products/{product_id}/")

def get_product(product_id: int, db = Depends(get_read_db))-> Optional[dict]:

    cached_product = cached_service.get_product(f'product:{product_id}')

    if cached_product:
        print(f"Возвращаю данные из кеша")
        return json.loads(cached_product)
    
    print(f"Кеш пуст, получаю данные из БД")
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail=f'Продукт с id: {product_id} не найден')

    product_data = {"id": product.id, "name": product.name, "price": float(product.price), "stock": product.stock}

    cached_service.set_product(product_id, product_data)
    return product_data


@app.post("/products/")

def add_new_product(product: AddProduct, db = Depends(get_write_db)):
    """Функция добавления нового продукта в таблицу products"""
    invalidate_cache('products:all')

    new_product = ProductModel(
        name=product.name,
        price=float(product.price),
        stock=product.stock
    )

    db.add(new_product)  # добавляю в БД
    db.commit()  # выполняю коммит для сохранения в БД
    db.refresh(new_product)  # получаю id

    # Возращаю добавленный продукт
    return {
        "id": new_product.id,
        "name": new_product.name,
        "price": float(new_product.price),
        "stock": new_product.stock,
        "message": f"Продутк {new_product.name} создан"
    }


# @app.patch("/products/{product_id}")
# def change_product(product_id: int, product_data: ProductPatch, db = Depends(get_write_db)):

#     # сначала проверим есть ли такой продукт
#     product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
#     if not product:
#         raise HTTPException(status_code=404, detail=f"Продукт с id: {product_id} не найден")
    
#     invalidate_cache('products:all')

