import random

class Market:
    def __init__(self, start_price=100):
        self.price = start_price
        self.trend = 0  # Represents market momentum

    def step(self):
        # Update the trend slightly randomly, creating momentum (uptrends/downtrends)
        self.trend += random.uniform(-0.1, 0.1)
        
        # Keep the trend within reasonable bounds roughly [-0.5, 0.5]
        self.trend = max(-0.5, min(0.5, self.trend))
        
        # Change price based on momentum plus some random noise
        change = self.trend + random.gauss(0, 0.2)
        self.price += change
        
        # Prevent prices from dropping arbitrarily low
        self.price = max(1.0, self.price)
        return self.price