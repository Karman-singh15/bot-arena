import gymnasium as gym
from gymnasium import spaces
import numpy as np
from market import Market

class TradingEnv(gym.Env):
    """
    A unified trading environment for OpenAI Gymnasium.
    This replaces the hardcoded bot behaviors with an environment suitable for RL training.
    """
    def __init__(self, initial_cash=1000.0, risk_tolerance=0.5):
        super(TradingEnv, self).__init__()
        
        # Action Space: 0 = HOLD, 1 = BUY, 2 = SELL
        self.action_space = spaces.Discrete(3)
        
        # Observation Space:
        # [current_price, trend_slope, cash, shares, average_buy_price, risk_tolerance]
        # We use a Box space for continuous values.
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(6,), dtype=np.float32
        )
        
        self.initial_cash = initial_cash
        self.risk_tolerance = risk_tolerance
        
        # Environment state
        self.market = None
        self.cash = 0.0
        self.shares = 0
        self.total_invested = 0.0
        self.price_history = []
        self.current_step = 0
        self.max_steps = 100  # length of one simulation episode
        
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        
        self.market = Market()
        self.cash = self.initial_cash
        self.shares = 0
        self.total_invested = 0.0
        self.price_history = [self.market.price]
        self.current_step = 0
        
        return self._get_obs(), {}
        
    def _get_obs(self):
        price = self.market.price
        
        # Calculate trend over the last 10 steps max
        history_window = self.price_history[-10:]
        trend = 0.0
        if len(history_window) >= 2:
            trend = history_window[-1] - history_window[0]
            
        avg_buy_price = 0.0
        if self.shares > 0:
            avg_buy_price = self.total_invested / self.shares
            
        return np.array([
            price,
            trend,
            self.cash,
            self.shares,
            avg_buy_price,
            self.risk_tolerance
        ], dtype=np.float32)
        
    def step(self, action):
        self.current_step += 1
        
        # Calculate net worth before we take any action or price changes
        prev_net_worth = self.cash + (self.shares * self.price_history[-1])
        
        # The market moves forward
        price = self.market.step()
        self.price_history.append(price)
        
        # Execute the chosen action
        # 0 = HOLD, 1 = BUY, 2 = SELL
        trade_executed = False
        if action == 1: # BUY
            if self.cash >= price:
                self.shares += 1
                self.cash -= price
                self.total_invested += price
                trade_executed = True
        elif action == 2: # SELL
            if self.shares > 0:
                avg_price = self.total_invested / self.shares
                self.shares -= 1
                self.cash += price
                self.total_invested -= avg_price
                trade_executed = True
                
        # Calculate new net worth
        current_net_worth = self.cash + (self.shares * price)
        
        # The reward is the delta in net worth over this step (profit/loss)
        reward = current_net_worth - prev_net_worth
        
        # Reward Shaping: Heavily encourage the bot to actually interact with the market
        if trade_executed:
            reward += 0.5  # Bonus for making a valid trade!
        elif action == 0:
            reward -= 0.1  # Slight penalty for just HOLDing (prevents lazy local minimum)
        else:
            reward -= 0.5  # Heavy penalty for picking BUY/SELL when it has no cash/shares
        
        terminated = False
        truncated = self.current_step >= self.max_steps
        
        info = {
            "net_worth": current_net_worth,
            "cash": self.cash,
            "shares": self.shares
        }
        
        return self._get_obs(), reward, terminated, truncated, info
