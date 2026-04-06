from src.models.exceptions import ValidationError
from fastapi import HTTPException


class User:
    # def __init__(self, name, email):
    #     self.name = name
    #     if not "@" in email:
    #         raise ValueError("Неверный формат email")
    #     self._email = email

    # def set_email(self, email):
    #     if "@" not in email:
    #         raise ValidationError("Неверный формат email")
    #     self._email = email


    # def __str__(self):
    #     return f"Пользователь: {self.name}, Email: {self._email}"
    # def get_user_by_id(conn, id):
    #     try:
    #         with conn.cursor() as cursor:
    #             cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    #             user = cursor.fetchone()
    #             if user is None:
    #                 raise 
    #             else:
    #                 return {
    #                         "id": user[0],
    #                         "name": user[1],
    #                         "email": user[2]
    #                         }
    #     except Exception:
    #         raise HTTPException(status_code=404, detail="Пользователь не найден")
    pass