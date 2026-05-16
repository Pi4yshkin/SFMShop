from pymongo import MongoClient
from pymongo.collection import Collection
from datetime import datetime
import os
from dotenv import load_dotenv
from typing import Optional


load_dotenv()

class ConnectToMongoDB:
    def __init__(self):
        self.client = MongoClient(
            host=os.getenv("MONGO_HOST", "localhost"),
            port=int(os.getenv("MONGO_PORT", 27017)))
        self.db = self.client["sfmshop_logs"]
        self.logs_collection = self.db["log"]

connection = ConnectToMongoDB()
logs_collection = connection.logs_collection

class AddOneLog:
    """Класс добавляет один лог"""
    def __init__(self, logs_collection: Collection):
        self.logs_collection = logs_collection

    def insert_one_log(self, log_data:dict)-> str:
        log = self.logs_collection.insert_one(log_data)
        return f"лог {log} успешно добавлен"

test_one_log = {
        "type": "error",
        "ip": "192.168.1.1",
        "message": "Ошибка подключения к БД",
        "timestamp": datetime(2024, 3, 17, 15, 30, 0),
        "stack_trace": "ConnectionError: timeout"
    }


class AddManyLogs:
    """Класс добавляет много логов"""
    def __init__(self, logs_collection: Collection):
        self.logs_collection = logs_collection

    def insert_many_logs(self, logs_data:list)-> bool:
        self.logs_collection.insert_many(logs_data)
        return True


class GetAllLogs:
    """Класс получает все логи"""
    def __init__(self, logs_collection: Collection):
        self.logs_collection = logs_collection

    def get_all_logs(self)-> list:
        logs = self.logs_collection.find()
        return list(logs)

# res = GetAllLogs(logs_collection)
# logs = res.get_all_logs()
# for log in logs:
#     print(f"[LOG]: {log}")

class GetLogsByFieldValue:
    """Класс получает логи по ключ: значению"""
    def __init__(self, logs_collection: Collection):
        self.logs_collection = logs_collection

    def get_log_by_field_value(self, field: str, value: str)->list:
        logs = self.logs_collection.find({str(field): value})
        return list(logs)

# res = GetLogsByFieldValue(logs_collection)
# logs = res.get_log_by_field_value("type", "access")
# for log in logs:
#     print(f"[LOG]: {log}")

class GetLogsByDate:
    """Класс получает логи по диапазону дат"""
    def __init__(self, logs_collection: Collection):
        self.logs_collection = logs_collection

    def get_logs_by_date(self, start_date: str, end_date: str, limit: Optional[int]=None)-> list:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        logs = self.logs_collection.find({"timestamp": {"$gte": start, "$lte": end}})

        if limit is not None:
            logs = logs.limit(limit)

        return list(logs)
    
# res = GetLogsByDate(logs_collection)
# logs = res.get_logs_by_date("2024-05-05", "2026-05-05", 2)
# for log in logs:
#     print(f"{log}")


class CountLogsByStatusCode:
    """Класс подсчета логов по статус коду"""
    def __init__(self, logs_collection: Collection):
        self.logs_collection = logs_collection

    def get_cnt_status_code(self, status_code: int)-> list:
        """Функция для подсчета логов по статус-коду"""
        pipeline = [
            {"$match": {"status_code": status_code}},
            {"$group": {
                "_id": "$status_code",
                "cnt": {"$sum": 1}}
                }
        ]
        logs = self.logs_collection.aggregate(pipeline)
        return list(logs)
    
# res = CountLogsByStatusCode(logs_collection)
# logs = res.get_cnt_status_code(200)
# for row in logs:
#     print(f"[LOG_cnt]: {row}")
    

class GetStatisticByYear:
    """Класс подсчета логов за указанный год"""
    def __init__(self, logs_collection: Collection):
        self.logs_collection = logs_collection

    def get_statistic_by_year(self, value: int)-> list:
        
        if not isinstance(value, int):
            value = int(value)

        pipeline = [
            {"$addFields": {"year": {"$year": "$timestamp"}}},  # <- главная жопаболь
            {"$match": {"year": value}},  # <- тут пытался искать отсортировать по {"$match": {"$year": value}}
            {"$count": "cnt"}
            
            ]
        result = self.logs_collection.aggregate(pipeline)
        return list(result)

# res = GetStatisticByYear(logs_collection)
# logs = res.get_statistic_by_year(2026)
# print(logs)


class DeleteAllLogs:
    """Класс удаляет все логи"""
    def __init__(self, logs_collection: Collection):
        self.logs_collection = logs_collection

    def delete_all_logs(self)-> bool:
        self.logs_collection.delete_many({})
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

class LogServices:
    def __init__(self, logs_collection: Collection):
        self.logs_collection = logs_collection
    
    def log_error(self, message, stack_trace):
        log_entry = {
            "type": "error",
            "message": message,
            "stack_trace": stack_trace,
            "timestamp": datetime.utcnow()
        }

        self.logs_collection.insert_one(log_entry)

    def log_access(self, ip: str, endpoint: str, method: str, status_code: int):
        log_entry = {
            "type": "access",
            "ip": ip,
            "endpoint": endpoint,
            "method": method,
            "status_code": status_code,
            "timestamp": datetime.utcnow()
        }

        self.logs_collection.insert_one(log_entry)

    def get_errors(self, limit: Optional[int] = None, since: Optional[datetime] = None):

        query = {"type": "error"}

        if since:
            query["timestamp"] = {"$gte": since}
        logs = self.logs_collection.find(query)

        if limit is not None:
            logs = logs.limit(limit)

        return list(logs)
        
    def get_access(self, limit: Optional[int] = None, since: Optional[datetime] = None):

        query = {"type": "access"}

        if since:
            query["timestamp"] = {"$gte": since}
        logs = self.logs_collection.find(query)

        if limit is not None:
            logs = logs.limit(limit)

        return list(logs)
    
log_service = LogServices(logs_collection)
# add_error_log = log_service.log_error("ошибка входа", "ConnectionError: timeout")
get_error_log = log_service.get_errors(limit=2)
for row in get_error_log:
    print(row)