class SFMShopException(Exception):
    """Базовое исключение для проекта SFMShop"""
    pass

class ValidationError(SFMShopException):
    """Ошибка валидации данных"""
    pass

class BusinessLogicError(SFMShopException):
    """Ошибка бизнес-логики"""
    pass

class GetInfoError(SFMShopException):
    """Ошибка получения информации"""
    pass
