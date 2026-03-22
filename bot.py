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
        self.total_invested = 0.0  # Track cost basis for calculating average buy price

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
        
        # New Profit-taking logic!
        # If the bot holds shares, the sell threshold should be based heavily on securing a profit
        # over its *average buy price*, augmented by the trend, instead of just the moving average.
        if self.shares > 0:
            average_buy_price = self.total_invested / self.shares
            # Base profit margin target: Conservative wants +2 points, Aggressive holds for +6 points
            profit_target = 2.0 + (self.risk_tolerance * 4.0)
            self.current_sell_threshold = average_buy_price + profit_target + (trend_adjustment * 0.5)
        else:
            # Fallback for display logging if no shares are held
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
            self.total_invested += price

        elif action == "SELL" and self.shares > 0:
            avg_price = self.total_invested / self.shares
            self.shares -= 1
            self.cash += price
            self.total_invested -= avg_price

import numpy as np
import os

class RLBot(Bot):
    def __init__(self, name, cash, risk_tolerance, model_path="ppo_trading_bot.zip"):
        super().__init__(name, cash, risk_tolerance)
        self.model = None
        
        if os.path.exists(model_path):
            try:
                from stable_baselines3 import PPO
                self.model = PPO.load(model_path)
                print(f"[{name}] Successfully loaded RL Model from {model_path}!")
            except Exception as e:
                print(f"[{name}] Warning: Could not load RL model: {e}")
        else:
            print(f"[{name}] Warning: Model file {model_path} not found. Bot will just HOLD.")
            
    def decide(self, price):
        self.price_history.append(price)
        if len(self.price_history) > 10:
            self.price_history.pop(0)

        # Fallback behavior if no model loaded
        if not self.model:
            return "HOLD"
            
        trend = 0.0
        if len(self.price_history) >= 2:
            trend = self.price_history[-1] - self.price_history[0]
            
        avg_buy_price = 0.0
        if self.shares > 0:
            avg_buy_price = self.total_invested / self.shares
            
        # Ensure obs matches what the TradingEnv expects:
        # [price, trend, cash, shares, avg_buy_price, risk_tolerance]
        obs = np.array([
            price,
            trend,
            self.cash,
            self.shares,
            avg_buy_price,
            self.risk_tolerance
        ], dtype=np.float32)
        
        action, _states = self.model.predict(obs, deterministic=True)
        # Actions: 0 = HOLD, 1 = BUY, 2 = SELL
        return ["HOLD", "BUY", "SELL"][action]

