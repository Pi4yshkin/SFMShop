from src.models.exceptions import ValidationError
"""
self -> сам дескриптор
instance -> экземпляр класса
owner -> класс
hasattr - проверить, есть ли атрибут
getattr - получить атрибут
setattr - установить значение атрибута
"""

class PositiveNumber:
    """Дескриптор для валидации положительных чисел"""

    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        """Получить значение"""
        return getattr(instance, self.name)
    
    def __set__(self, instance, value):
        """Установить значение или выбросить исключение"""
        if value <= 0:
            raise ValidationError(f"Значение '{self.name}': {value} должно быть положительным!")
        setattr(instance, self.name, value)

    def __call__(self, value):
        if not isinstance(value, (int, float)):
            raise ValidationError(f"Значение  должно быть числом!")
        if value <= 0:
            raise ValidationError(f"Значение  должно быть положительным!")
        return value 


class CachedProperty:
    """Дескриптор кеширования"""
    def __init__(self, func):
        self.func = func
        self.name = func.__name__

    def __get__(self, instance, owner):
        if instance is None:
            return self
        
        # Поиск значения в кеше
        _cashed_attr = f"_cashed_{self.name}"
        if hasattr(instance, _cashed_attr):
            return getattr(instance, _cashed_attr)
        
        # Если нет, вычисляем и добавляем в кеш
        value = self.func(instance)
        setattr(instance, _cashed_attr, value)
        return value