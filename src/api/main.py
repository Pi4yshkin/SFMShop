from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from src.database.connection import connect_to_db, get_user_by_id, get_product_by_id, get_all_products
import psycopg2
from src.models.product import Product
from src.models.order import Order
from fastapi.testclient import TestClient


app = FastAPI()

@app.on_event("startup")
async def startup():
    global conn
    conn = connect_to_db(host="localhost", database="sfmshop", user="postgres", password="DiggerLLP199222")


@app.get("/products", status_code=200) 
def get_products(limit: int=10, offset: int=0):  # limit - кол-во товаров на странице, offset - с какого товара начинать
    try:
        all_products = Product.get_products_(conn, limit, offset)  # Получаем все товары из базы данных через метод класса Product

        products = [] # Инициализируем список products, который будет содержать все товары из базы данных
        for data in all_products:  
            product = Product(data[1], data[2], data[3])  # Создаю экземпляр класса Product для каждого товара из базы данных
            product.id = data[0]  # Устанавливаем id товара из базы данных(выносим отдельно из-за того, что id SERIAL PRIMARY KEY и если указать product = Product(data[0], data[1], data[2], data[3]) -> исключение: ожидает 4 аргумента, а передаем 5)
            products.append(product.__dict__)  # Преобразуем каждый товар в словарь и добавляем в список

        total = len(products)  # Общее количество товаров
        if total == 0:  
            raise HTTPException(status_code=404, detail="Товаров нет")
        if offset > total:
            raise HTTPException(status_code=500, detail="offset > total, саписок товаров пуст!")
        if limit <= 0:
            raise HTTPException(status_code=500, detail="limit <= 0, саписок товаров пуст!")

        return {"total": total,
                "limit": limit,
                "offset": offset,
                "products": products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# @app.get("/products", status_code=200)
# def get_products(conn):
#     try:
#         products = get_all_products(conn)

#         all_products = []

#         for data in products:
#             product = dict(id=data[0], name=data[1], price=data[2], quantity=data[3])
#             all_products.append(product)

#         return all_products
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


@app.get("/products/{id}")
def get_product(id: int):
    try:
        product = get_product_by_id(conn, id)
        if product is None: 
            raise HTTPException(status_code=404, detail=f"Товар не найден")
        else:
            return product
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.put("/products/{product_id}", status_code=200)
def update_product(product_id: int, product_data: dict):
    try:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE products SET name = %s, price = %s, quantity = %s WHERE id = %s", (product_data['name'], product_data['price'], product_data['quantity'], product_id))
            if cursor.rowcount <= 0:
                raise HTTPException(status_code=404, detail="Товар не найден")
            conn.commit()
        return { 
            "product_id": product_id, 
            "message": "Продукт изменен"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/products/{product_id}", status_code=200)
def delete_product(product_id: int):
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
            if cursor.rowcount <= 0:
                raise HTTPException(status_code=404, detail="Товар не найден")
            conn.commit()
            return {"message": "Товар удален"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class OrderCreate(BaseModel):
    user_id: int
    total: float


@app.post("/orders", status_code=201)
def create_order(order: OrderCreate):
    try:
        add_order = Order.add_order(conn, order.user_id, order.total)
        return {
                "message": "Заказ создан",
                "user_id": order.user_id, 
                "total": order.total
                }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users")
def get_users():
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/{id}")
def get_user(id: int):
    try:
        user = get_user_by_id(conn, id)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сервера {e}")
    
class CreateUser(BaseModel):
    name: str
    email: EmailStr

@app.post("/users", status_code=201)
def create_user(user: CreateUser):
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (user.name, user.email))
            conn.commit()
        return {"name": user.name, "email": user.email}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.on_event("shutdown")
async def shutdown():
    if conn:
        conn.close()

