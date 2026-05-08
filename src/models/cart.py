

class ShoppingCart:
    """Класс корзина с товарами"""
    def __init__(self):
        self.items = []  # создаю изначально пустую корзину

    def __add__(self, item):
        """Реализация создания пустой корзины и добавления товаров"""
        new_cart = ShoppingCart()  # создаю объект(экземпляр)
        new_cart.items = self.items.copy()  # создаю копию, что бы не менять исходную корзину
        new_cart.items.append(item)  # добавляю продукт
        return new_cart
    
    def __len__(self):
        """Реализация подсчета товаров в корзине"""
        return len(self.items)
    
    def __iter__(self):
        """Реализация итератора"""
        return iter(self.items)  

    def __str__(self):
        return f"Товаров в корзине: {len(self.items)}"
    


    