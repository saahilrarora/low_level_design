from enum import Enum

class Denomination(Enum):
    QUARTER = 0.25
    HALFDOLLAR = 0.5
    DOLLAR = 1.0
    FIVEDOLLARS = 5.0

class Product:
    def __init__(self, name, cost, quantity=10):
        self.name = name
        self.cost = cost
        self.quantity = quantity

    def remove(self) -> None:
        if self.quantity:
            self.quantity -= 1
    
    def restock(self) -> None:
        # assuming no cap for now
        self.quantity += 1

class VendingMachine:
    def __init__(self):
        self.products = [["chips", 1.50], ["soda", 2], ["candy", 1], ["water", 1.25], ["cookies", 1.75]]
        self.mapping = {}
        self.bank = {"quarters":20, "half-dollars":10, "dollar":5, "five-dollars":0}
        row = "A"
        col = 1

        for product, cost in self.products:
            newProduct = Product(product, cost)
            self.mapping[row+str(col)] = newProduct
            col += 1
    
    def validateProduct(self, cell) -> bool:
        if cell in self.mapping and self.mapping[cell].quantity > 0:
            return True
        return False

    def checkout(self, cell, quarters, halfDollar, dollar, fiveDollars) -> bool:
        if not self.validateProduct(cell):
            return False
        
        product = self.mapping[cell]
        if self.dispenseChange(product.cost, quarters, halfDollar, dollar, fiveDollars) == -1.0:
            return False
        
        return True      

    def dispenseChange(self, cost, quarters, halfDollar, dollar, fiveDollars) -> float:
        money = (0.25*quarters) + (0.5*halfDollar) + dollar + (5*fiveDollars)

        # check for total money first
        if money < cost:
            return -1.0
        
        # now we want to check for whether we can accurately give back the change
        # the largest amount of change we can give is 5-1 = 4 dollars
        # before we add to our bank, we want to make sure we can give back correct change
        # we should always use as many dollars as possible first
        # convert to cents to avoid floating point issues
        change = round((money - cost) * 100)

        # greedy: try largest denominations first
        # each tuple is (cent value, bank key)
        denominations = [
            (100, "dollar"),
            (50, "half-dollars"),
            (25, "quarters"),
        ]

        for cent_value, key in denominations:
            # how many of this coin can we use? min of what we need and what we have
            coins_needed = change // cent_value
            coins_available = self.bank[key]
            coins_used = min(coins_needed, coins_available)

            change -= coins_used * cent_value
            self.bank[key] -= coins_used

        # if change isn't 0, we couldn't make exact change — undo everything and fail
        if change != 0:
            # TODO: ideally roll back the bank deductions here
            return -1.0

        # success — add the customer's money to the bank
        self.bank["quarters"] += quarters
        self.bank["half-dollars"] += halfDollar
        self.bank["dollar"] += dollar

        return 0.0
