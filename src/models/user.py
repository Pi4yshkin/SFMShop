from src.models.descriptors import PositiveNumber
from src.models.mixins import SerializableMixin
from src.models.metaclasses import ModelMeta



class User(SerializableMixin, metaclass=ModelMeta):
    user_id = PositiveNumber("_user_id")
    age = PositiveNumber("_age")  # Убеждаемся, что возраст != 0 и не отрицательный
    balance = PositiveNumber("_balance")

    def __init__(self, user_id, name, email, age, balance):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.age = age
        self.balance = balance
        self.orders = []
        self.is_active = True

    def to_json(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "age": self.age,
            "balance": self.balance,
            "orders": self.orders,
            "is_active": self.is_active
        }
    
    def __str__(self):
        return f"Пользователь: {self.name}, id #{self.user_id}, email: {self.email}, возраст: {self.age}, баланс: {self.balance}, активность профиля: {self.is_active}"

class UserValidator:
    def validate_user(user: User) -> bool:
        """Валидация пользователя"""
        if not user.name:
            raise ValueError("Имя не может быть пустым")
        if "@" not in user.email:
            raise ValueError("Email должен содержать @")
        if user.age < 18:
            raise ValueError("Пользователь должен быть старше 18 лет")
        if user.balance < 0:
            raise ValueError("Баланс не может быть отрицательным")
        return True

