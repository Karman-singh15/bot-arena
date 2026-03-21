class Bot:
    def __init__(self, name, cash, risk_tolerance):
        self.name = name
        self.cash = cash
        self.shares = 0
        self.risk_tolerance = risk_tolerance

    def decide(self, price):
        # very simple logic for now
        if price < 100 and self.cash > price:
            return "BUY"
        elif price > 102 and self.shares > 0:
            return "SELL"
        return "HOLD"

    def act(self, action, price):
        if action == "BUY" and self.cash >= price:
            self.shares += 1
            self.cash -= price

        elif action == "SELL" and self.shares > 0:
            self.shares -= 1
            self.cash += price

