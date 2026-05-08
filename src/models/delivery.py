from abc import ABC, abstractmethod


class Delivery(ABC):

    @abstractmethod
    def delivery_cost(self, distance: float) -> float:
        pass


class StandartDelivery(Delivery):

    def delivery_cost(self, distance: float) -> float:
        return distance * 10
    

class ExpressDelivery(Delivery):

    def delivery_cost(self, distance: float) -> float:
        return distance * 20
    
    
def delivery_calculation(delivery: Delivery):

    return delivery.delivery_cost(130)


standart_delivery = StandartDelivery()
express_delivery = ExpressDelivery()

print(delivery_calculation(standart_delivery))
print(delivery_calculation(express_delivery))