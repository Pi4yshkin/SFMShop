from abc import ABC, abstractmethod


class DeliveryStrategy(ABC):
    """Абстрактный класс для работы с доставкой"""

    @abstractmethod
    def calculate_cost(distance: float):
        pass

class StandartDelivery(DeliveryStrategy):
    """Расчет стандартной доставки"""

    def calculate_cost(distance: float)-> float:
        return distance * 10
    
class ExpressDelivery(DeliveryStrategy):
    """Расчет эксперсс доставки"""

    def calculate_cost(distance: float)-> float:
        return distance * 20