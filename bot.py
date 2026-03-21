class Bot:
    def __init__(self, name, cash, risk_tolerance):
        self.name = name
        self.cash = cash
        self.shares = 0
        self.risk_tolerance = risk_tolerance

    def decide(self, price):
        # Adjust thresholds based on risk_tolerance
        # Conservative bots (low risk_tolerance) demand lower prices to buy and sell quickly
        # Aggressive bots (high risk_tolerance) buy closer to base price and hold for larger gains
        buy_threshold = 95 + (self.risk_tolerance * 5)
        sell_threshold = 101 + (self.risk_tolerance * 5)
        
        if price < buy_threshold and self.cash >= price:
            return "BUY"
        elif price > sell_threshold and self.shares > 0:
            return "SELL"
        return "HOLD"

    def act(self, action, price):
        if action == "BUY" and self.cash >= price:
            self.shares += 1
            self.cash -= price

        elif action == "SELL" and self.shares > 0:
            self.shares -= 1
            self.cash += price

