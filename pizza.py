# Pizza class
class Pizza:
    def __init__(self, size, crust, toppings):
        if size not in {"small", "medium", "large"}:
            raise ValueError(f"Invalid size: {size}")
        if crust not in {"thin", "thick", "stuffed"}:
            raise ValueError(f"Invalid crust: {crust}")
        self.size = size
        self.crust = crust
        self.toppings = set(toppings)
    
    def add_topping(self, topping) -> None:
        self.toppings.add(topping)
    
    def remove_topping(self, topping) -> None:
        if topping in self.toppings:
            self.toppings.remove(topping)
            
class Prices:
    def __init__(self):
        self.toppings = {"cheese": 1, "pepporoni": 2, "mushrooms": 1.50, "olives":1}
        self.sizing = {"small": 8, "medium": 10, "large":12}
        self.tax = 1.10

class Order:
    def __init__(self, pizzas) -> None:
        self.pizzas = pizzas
        self.prices = Prices()
    
    def calculate(self):
        totalPrice = 0
        for pizza in self.pizzas:
            for topping in pizza.toppings:
                if topping in self.prices.toppings:
                    totalPrice += self.prices.toppings[topping]
            totalPrice += self.prices.sizing[pizza.size]
        
        totalPrice *= self.prices.tax
        return totalPrice

