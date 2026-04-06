import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from src.api.main import app, startup, shutdown
import asyncio


async def init_db():
    await startup()

async def close_db():
    await shutdown()

asyncio.run(init_db())

client = TestClient(app)

def test_get_products():
    response = client.get("/products")
    assert response.status_code == 200
    print("✅ GET products: OK")

def test_get_product_by_id():
    response = client.get("/products/1")
    assert response.status_code == 200
    print("✅ GET products/1: OK")

def test_delete_product():
    response = client.delete("/products/1")
    assert response.status_code == 200
    print("✅ DELETE products/1: OK")

def test_create_order():
    response = client.post("/orders", json={"user_id": 1, "total": 12000})
    assert response.status_code == 201
    print("✅ POST orders: OK")

def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    print("✅ GET users: OK")

def test_get_user_by_id():
    response = client.get("/users/1")
    assert response.status_code == 200
    print("✅ GET users/1: OK")

def test_create_user():
    response = client.post("/users", json={"name": "Voland", "email": "voland@test.com"})
    assert response.status_code == 201
    print("✅ POST users: OK")

if __name__ == "__main__":
    
    tests = [
        test_get_products,
        test_get_product_by_id,
        test_delete_product,
        test_create_order,
        test_get_users,
        test_get_user_by_id,
        test_create_user
    ]
    
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"❌ Тест не пройден: {e}")
        except Exception as e:
            print(f"❌ Ошибка в тесте {test.__name__}: {e}")

