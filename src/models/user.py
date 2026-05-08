from src.models.exceptions import ValidationError


class User:
    def __init__(self, name, email):
        self.name = name
        if not "@" in email:
            raise ValueError("Неверный формат email")
        self._email = email

    def set_email(self, email):
        if "@" not in email:
            raise ValidationError("Неверный формат email")
        self._email = email


    def __str__(self):
        return f"Пользователь: {self.name}, Email: {self._email}"