from src.models.metaclasses import ModelMeta
from src.models.descriptors import PositiveNumber
from src.models.mixins import LoggableMixin, SerializableMixin


class Order(LoggableMixin, SerializableMixin, metaclass=ModelMeta):
    order_id = PositiveNumber("_order_id")

    def __init__(self, order_id, items, user):
        self.order_id = order_id
        self.items = items
        self.user = user

        self.log(f"Заказ создан. ID: {order_id}")

    def to_json(self):
        return {
            "order_id": self.order_id,
            "items": self.items,
            "user": self.user
        }


    def __lt__(self, other):
        if not isinstance(other, Order):
            return NotImplemented
        return self.order_id < other.order_id
    
    def __contains__(self, item):
        return item in self.items
    
    def __len__(self):
        return len(self.items)
    
    def __add__(self, other):
        if not isinstance(other, Order):
            return NotImplemented
        new_items = self.items + other.items
        return Order(self.order_id, new_items, self.user)
    
    def __str__(self):
        return f"{self.user}, id #{self.order_id} с товарами {self.items}"
    
    def __repr__(self):
        return f"Order(user:{self.user}, id:{self.order_id}, товары:{self.items})"