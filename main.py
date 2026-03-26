from src.database.connection import connect_to_db
from src.database.connection import add_product
from src.database.connection import get_products
from src.database.connection import update_product_price


conn = connect_to_db("localhost", "sfmshop", "postgres", "DiggerLLP199222")

# add_product(conn, "Клавиатура", 3000, 34)

products = get_products(conn)
print("Все товары:")
for product in products:
    print(*product)

update_product_price(conn, 1, 50_000)
