from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# подключаемся к БД
client = MongoClient(
    host=os.getenv("MONGO_HOST", "localhost"),
    port=int(os.getenv("MONGO_PORT", 27017))
)

# выбор БД
db = client["sfmshop_logs"]

# выбор коллекции
logs_collection = db["log"]


def insert_one_log(log_data:dict)-> str:
    """Функция добавления одного лога"""
    log = logs_collection.insert_one(log_data)
    return f"лог {log} успешно добавлен"

test_one_log = {
        "type": "error",
        "ip": "192.168.1.1",
        "message": "Ошибка подключения к БД",
        "timestamp": datetime(2024, 3, 17, 15, 30, 0),
        "stack_trace": "ConnectionError: timeout"
    }

# print(insert_one_log(test_one_log))

def insert_many_logs(logs_data:list)-> bool:
    logs_collection.insert_many(logs_data)
    return True


def get_all_logs()-> list:
    """Функция получения всех логов"""
    logs = logs_collection.find()
    return list(logs)

# all_logs = get_all_logs()
# for log in all_logs:
#     print(f"[LOG]: {log}")

def get_log_by_fiel_value(field: str, value: str)->list:
    """Функция получения логов по ключ: значению, первым аргументов указывается поле, вторым - значение.
    Функция для задания поиска логов по статус-коду и IP(но это если нам известны оба значения)"""
    logs = logs_collection.find({str(field): value})
    return list(logs)

# result = get_log_by_fiel_value("type", "access")
# for log in result:
#     print(f"[LOG]: {log}")

def get_logs_by_date(start_date: str, end_date: str)-> list:
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)
    logs = logs_collection.find({"timestamp": {"$gte": start, "$lte": end}})
    return list(logs)

# result_date_logs = get_logs_by_date("2024-05-09 00:00", "2026-05-09 00:00")
# for log in result_date_logs:
#     print(f"[DATE_LOG]: {log}")

def get_cnt_status_code(status_code: int)-> list:
    """Функция для подсчета логов по статус-коду"""
    pipeline = [
        {"$match": {"status_code": status_code}},
         {"$group": {
             "_id": "$status_code",
             "cnt": {"$sum": 1}}
             }
    ]
    result = logs_collection.aggregate(pipeline)
    return list(result)
    
# result_cnt_status_code = get_cnt_status_code(200)
# print(result_cnt_status_code)

def get_statistic_by_year(value: int)-> list:
    """Функция подсчета логов за указанный год"""
    if not isinstance(value, int):
        value = int(value)

    pipeline = [
        {"$addFields": {"year": {"$year": "$timestamp"}}},  # <- главная жопаболь
        {"$match": {"year": value}},  # <- тут пытался искать отсортировать по {"$match": {"$year": value}}
        {"$count": "cnt"}
        
        ]
    result = logs_collection.aggregate(pipeline)
    return list(result)

if __name__ == "__main__":  # <- до сих пор не понимаю для чего использовать, надо еще раз загуглить
    result_statistic_by_year = get_statistic_by_year(2025)
    print(result_statistic_by_year)


def delete_all_logs()-> bool:
    logs_collection.delete_many({})
    return True




test_logs = [
    {
        "type": "error",
        "message": "Ошибка подключения к БД",
        "timestamp": datetime(2024, 1, 15, 10, 30, 0),
        "stack_trace": "ConnectionError: timeout"
    },
    {
        "type": "access",
        "ip": "192.168.1.1",
        "endpoint": "/api/products",
        "method": "GET",
        "status_code": 200,
        "timestamp": datetime(2024, 2, 20, 15, 45, 0)
    },
    {
        "type": "warning",
        "message": "Медленный запрос",
        "duration_ms": 5000,
        "endpoint": "/api/users",
        "timestamp": datetime(2024, 3, 10, 9, 15, 30)
    },
    {
        "type": "error",
        "message": "404 Not Found",
        "endpoint": "/page/123",
        "ip": "10.0.0.1",
        "timestamp": datetime(2024, 4, 5, 23, 50, 15)
    },
    {
        "type": "access",
        "ip": "10.0.0.5",
        "endpoint": "/api/login",
        "method": "POST",
        "status_code": 201,
        "timestamp": datetime(2024, 5, 12, 8, 0, 0)
    },
    {
        "type": "info",
        "message": "Сервер запущен",
        "port": 8080,
        "timestamp": datetime(2024, 6, 1, 0, 0, 0)
    },
    {
        "type": "error",
        "message": "Критическая ошибка памяти",
        "memory_used": 4096,
        "timestamp": datetime(2024, 7, 20, 14, 30, 0)
    },
    {
        "type": "access",
        "ip": "192.168.1.100",
        "endpoint": "/api/orders",
        "method": "GET",
        "status_code": 200,
        "timestamp": datetime(2024, 8, 3, 11, 20, 0)
    },
    {
        "type": "warning",
        "message": "Подозрительная активность",
        "ip": "45.67.89.10",
        "attempts": 5,
        "timestamp": datetime(2024, 9, 14, 18, 45, 0)
    },
    {
        "type": "info",
        "message": "Резервное копирование завершено",
        "size_mb": 1024,
        "timestamp": datetime(2024, 10, 25, 2, 0, 0)
    },
    {
        "type": "error",
        "message": "Таймаут запроса к API",
        "timeout_seconds": 30,
        "timestamp": datetime(2024, 11, 7, 13, 15, 0)
    },
    {
        "type": "access",
        "ip": "8.8.8.8",
        "endpoint": "/api/search",
        "method": "GET",
        "status_code": 200,
        "timestamp": datetime(2024, 12, 24, 10, 5, 0)
    },
    {
        "type": "info",
        "message": "Новый пользователь зарегистрирован",
        "user_id": "user_12345",
        "timestamp": datetime(2025, 1, 5, 16, 30, 0)
    },
    {
        "type": "error",
        "message": "Ошибка валидации данных",
        "field": "email",
        "value": "invalid",
        "timestamp": datetime(2025, 2, 14, 9, 45, 0)
    },
    {
        "type": "warning",
        "message": "Заканчивается место на диске",
        "free_space_gb": 5,
        "timestamp": datetime(2025, 3, 30, 22, 0, 0)
    },
    {
        "type": "access",
        "ip": "192.168.1.50",
        "endpoint": "/api/profile",
        "method": "PUT",
        "status_code": 200,
        "timestamp": datetime(2025, 4, 18, 11, 30, 0)
    }
]
# print(delete_all_logs())
# print(insert_many_logs(test_logs))