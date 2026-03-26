import psycopg2


def connect_to_db(host, database, user, password):
    with psycopg2.connect(host=host,
                          database=database,
                          user=user,
                          password=password) as conn:
        return conn

def add_product(conn, name, price, quantity):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)", (name, price, quantity))

        conn.commit()

def get_products(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM products")

        products = cursor.fetchall()

        return products

def update_product_price(conn, product_id, new_price):
    with conn.cursor() as cursor:
        cursor.execute("UPDATE products SET price = %s WHERE id = %s", (new_price, product_id))
        conn.commit()

