class LoggableMixin:
    def log(self, message: str):
        print(f"[{self.__class__.__name__}] {message}")


class ValidatableMixin:
    def validate(self):
        return True
    
    def is_valid(self):
        try:
            self.validate()
            return True
        except ValueError:
            return False
    

class SerializableMixin:
    def to_json(self):
        return {
            "class": self.__class__.__name__,
            "data": self.__dict__
        }
