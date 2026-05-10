"""На данный момент структура БД проекта SFMShop выглядит следующим образом:
sfmshop=# \d
                     Список отношений
 Схема  |       Имя       |        Тип         | Владелец 
--------+-----------------+--------------------+----------
 public | orders          | таблица            | postgres
 public | orders_id_seq   | последовательность | postgres
 public | products        | таблица            | postgres
 public | products_id_seq | последовательность | postgres
 public | reviews         | таблица            | postgres
 public | reviews_id_seq  | последовательность | postgres
 public | users           | таблица            | postgres
 public | users_id_seq    | последовательность | postgres
(8 строк)

sfmshop=# \d orders;
                                                Таблица "public.orders"
  Столбец   |             Тип             | Правило сортировки | Допустимость NULL |            По умолчанию            
------------+-----------------------------+--------------------+-------------------+------------------------------------
 id         | integer                     |                    | not null          | nextval('orders_id_seq'::regclass)
 user_id    | integer                     |                    |                   | 
 product_id | integer                     |                    |                   | 
 total      | numeric(10,2)               |                    | not null          | 
 created_at | timestamp without time zone |                    |                   | CURRENT_TIMESTAMP
Индексы:
    "orders_pkey" PRIMARY KEY, btree (id)
    "idx_user_id" btree (user_id)
Ограничения внешнего ключа:
    "orders_product_id_fkey" FOREIGN KEY (product_id) REFERENCES products(id)
    "orders_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id)

sfmshop=# \d products;
                                                Таблица "public.products"
  Столбец   |             Тип             | Правило сортировки | Допустимость NULL |             По умолчанию             
------------+-----------------------------+--------------------+-------------------+--------------------------------------
 id         | integer                     |                    | not null          | nextval('products_id_seq'::regclass)
 name       | character varying(100)      |                    | not null          | 
 price      | numeric(10,2)               |                    | not null          | 
 quantity   | integer                     |                    |                   | 0
 created_at | timestamp without time zone |                    |                   | CURRENT_TIMESTAMP
Индексы:
    "products_pkey" PRIMARY KEY, btree (id)
Ссылки извне:
    TABLE "orders" CONSTRAINT "orders_product_id_fkey" FOREIGN KEY (product_id) REFERENCES products(id)
    TABLE "reviews" CONSTRAINT "reviews_product_id_fkey" FOREIGN KEY (product_id) REFERENCES products(id)

sfmshop=# \d users;
                                                Таблица "public.users"
  Столбец   |             Тип             | Правило сортировки | Допустимость NULL |           По умолчанию            
------------+-----------------------------+--------------------+-------------------+-----------------------------------
 id         | integer                     |                    | not null          | nextval('users_id_seq'::regclass)
 name       | character varying(100)      |                    | not null          | 
 email      | character varying(100)      |                    | not null          | 
 balance    | numeric(10,2)               |                    | not null          | 0
 created_at | timestamp without time zone |                    |                   | CURRENT_TIMESTAMP
Индексы:
    "users_pkey" PRIMARY KEY, btree (id)
    "idx_name" btree (name)
    "users_email_key" UNIQUE CONSTRAINT, btree (email)
Ссылки извне:
    TABLE "orders" CONSTRAINT "orders_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id)
    TABLE "reviews" CONSTRAINT "reviews_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id)

sfmshop=# \d reviews;
                                                 Таблица "public.reviews"
   Столбец   |             Тип             | Правило сортировки | Допустимость NULL |            По умолчанию             
-------------+-----------------------------+--------------------+-------------------+-------------------------------------
 id          | integer                     |                    | not null          | nextval('reviews_id_seq'::regclass)
 user_id     | integer                     |                    |                   | 
 product_id  | integer                     |                    |                   | 
 review_text | text                        |                    |                   | 
 rating      | integer                     |                    | not null          | 
 created_at  | timestamp without time zone |                    |                   | CURRENT_TIMESTAMP
Индексы:
    "reviews_pkey" PRIMARY KEY, btree (id)
Ограничения-проверки:
    "reviews_rating_check" CHECK (rating >= 1 AND rating <= 5)
Ограничения внешнего ключа:
    "reviews_product_id_fkey" FOREIGN KEY (product_id) REFERENCES products(id)
    "reviews_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id)

    
Предложения по денормализации:
- в таблице orders добавить поля user_name и product_name для отчета
- в таблице reviews добавить поле product_name

Триггер для user_name таблицы orders:
CREATE OR REPLACE FUNCTION update_orders_user_name()
RETURNS TRIGGER AS $$
BEGIN
UPDATE orders SET user_name = NEW.name WHERE user_id = NEW.id;
RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER change_orders_user_name
AFTER UPDATE ON users
FOR EACH ROW
WHEN (OLD.name IS DISTINCT FROM NEW.name)
EXECUTE FUNCTION update_orders_user_name;

Триггер для product_name таблицы orders:
CREATE OR REPLACE FUNCTION update_orders_product_name()
RETURNS TRIGGER AS $$
BEGIN
UPDATE orders SET product_name = NEW.name WHERE product_id = NEW.id;
RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER change_product_name
AFTER UPDATE ON products
FOR EACH ROW
WHEN (OLD.name IS DISTINCT FROM NEW.name)
EXECUTE FUNCTION update_orders_product_name()

Триггер для product_name таблицы reviews:
CREATE OR REPLACE FUNCTION update_reviews_product_name()
RETURNS TRIGGER AS $$
BEGIN
UPDATE reviews SET product_name = NEW.name WHERE product_id = NEW.id;
RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER change_product_name
AFTER UPDATE ON products
FOR EACH ROW
WHEN (OLD.name IS DISTINCT FOR NEW.name)
EXECUTE FUNCTION update_reviews_product_name()

Компромисс: убрать JOIN для получения имени пользователя и названия товара для таблицы orders

Компромисс: убрать JOIN для получения названия товара при запросе отзывов

PS триггеры писал по примеру из урока, надеюсь задачи с ними будут в будущем.
PSS закинул свой анализ для анализа в дипсик, тот наругался. говорит тут ничего не надо денормализовать :D
"""