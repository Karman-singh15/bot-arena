import random

class Market:
    def __init__(self, start_price=100):
        self.price = start_price

    def step(self):
        change = random.uniform(-1, 1)  # small fluctuation
        self.price += change
        return self.price