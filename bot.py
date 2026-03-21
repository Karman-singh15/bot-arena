class Bot:
    def __init__(self, name, cash, risk_tolerance):
        self.name = name
        self.cash = cash
        self.shares = 0
        self.risk_tolerance = risk_tolerance
        self.price_history = []  # Keep track of recent prices to learn the trend

    def decide(self, price):
        # Learn the pattern by updating our history
        self.price_history.append(price)
        if len(self.price_history) > 10:
            self.price_history.pop(0)
            
        # If we don't have enough history to see a trend, just wait
        if len(self.price_history) < 5:
            return "HOLD"
            
        # Calculate trailing moving average to find the current 'base' value
        moving_average = sum(self.price_history) / len(self.price_history)
        
        # Notice the overall trend pattern over our history window
        trend_pattern = self.price_history[-1] - self.price_history[0]
        
        # Smart adaptation: Bots adjust to the pattern! 
        # Aggressive bots will heavily increase their thresholds to "chase" a strong uptrend
        # Conservative bots are less impressed by hype and stick closer to the baseline
        trend_adjustment = trend_pattern * self.risk_tolerance 
        
        # Adjust thresholds relative to the moving trend + the learned pattern adjustment
        buy_threshold = moving_average - 2.0 + (self.risk_tolerance * 3.0) + trend_adjustment
        
        # Same logic for selling, ensuring they don't sell too early during an uptrend
        sell_threshold = moving_average + 1.0 + (self.risk_tolerance * 2.0) + trend_adjustment
        
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

