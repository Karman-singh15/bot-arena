class Bot:
    def __init__(self, name, cash, risk_tolerance):
        self.name = name
        self.cash = cash
        self.shares = 0
        self.risk_tolerance = risk_tolerance
        self.price_history = []  # Keep track of recent prices to learn the trend
        self.current_trend = 0.0
        self.current_buy_threshold = 0.0
        self.current_sell_threshold = 0.0

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
        self.current_trend = self.price_history[-1] - self.price_history[0]
        
        # Smart adaptation: Bots adjust to the pattern! 
        # All bots now heavily factor in the trend (baseline of 0.8 multiplier),
        # but aggressive bots still factor it in more.
        trend_multiplier = 0.8 + (self.risk_tolerance * 0.5)
        
        if self.current_trend > 0:
            # In a bull market, they eagerly chase the rally
            trend_adjustment = self.current_trend * trend_multiplier
        else:
            # In a bear market, dampen the fear so their thresholds don't drop 
            # impossibly low. This keeps them 'in range' to buy the dip!
            trend_adjustment = self.current_trend * trend_multiplier * 0.4
            
        # Adjust thresholds relative to the moving trend + the learned pattern adjustment
        # Reduced the flat negative offset (-1.0 instead of -2.0) so conservative bots aren't left behind.
        self.current_buy_threshold = moving_average - 1.0 + (self.risk_tolerance * 2.0) + trend_adjustment
        
        # Same logic for selling, ensuring they don't sell too early during an uptrend
        self.current_sell_threshold = moving_average + 1.0 + (self.risk_tolerance * 2.0) + trend_adjustment
        
        if price < self.current_buy_threshold and self.cash >= price:
            return "BUY"
        elif price > self.current_sell_threshold and self.shares > 0:
            return "SELL"
        return "HOLD"

    def act(self, action, price):
        if action == "BUY" and self.cash >= price:
            self.shares += 1
            self.cash -= price

        elif action == "SELL" and self.shares > 0:
            self.shares -= 1
            self.cash += price

