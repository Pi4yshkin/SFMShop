from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from src.database.connection import connect_to_db
import psycopg2
from src.models.product import Product


app = FastAPI()
@app.get("/products")
def get_products(limit: int=10, offset: int=0, conn = Depends(connect_to_db)):  # limit - кол-во товаров на странице, offset - с какого товара начинать
    with conn.cursor() as cursor:
        try:
            all_products = Product.get_all_products(conn)  # Получаем все товары из базы данных через метод класса Product
            total = len(all_products)  # Общее количество товаров
            products = all_products[offset:offset+limit]  # Получаем товары для текущей страницы
            return {"total": total,
                    "limit": limit,
                    "offset": offset,
                    "products": products}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    


@app.get("/products/{id}")
def get_product(id: int, conn = Depends(connect_to_db)):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
        product = cursor.fetchone()
    if product is None: 
        raise HTTPException(status_code=404, detail=f"Товар с id={id} не найден")
    else:
        return product
    

class OrderCreate(BaseModel):
    user_id: int
    total: float


@app.post("/orders", status_code=201)
def create_order(order: OrderCreate, conn = Depends(connect_to_db)):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO orders (user_id, total) VALUES (%s, %s)", (order.user_id, order.total))
        conn.commit()
    return {"message": "Заказ создан", "user_id": order.user_id, "total": order.total}

@app.get("/users")
def get_users(conn = Depends(connect_to_db)):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
    return users

@app.get("/users/{id}")
def get_user(id: int, conn = Depends(connect_to_db)):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
        user = cursor.fetchone()
    if user is None:
        raise HTTPException(status_code=404, detail=f"Пользователь с id={id} не найден")
    else:
        return user
    
class CreateUser(BaseModel):
    name: str
    email: EmailStr

@app.post("/users", status_code=201)
def create_user(user: CreateUser, conn = Depends(connect_to_db)):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (user.name, user.email))
        conn.commit()
    return {"name": user.name, "email": user.email}
