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
        # [price, short_trend, long_trend, cash, shares, average_buy_price, risk_tolerance]
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(7,), dtype=np.float32
        )
        
        self.initial_cash = initial_cash
        self.risk_tolerance = risk_tolerance
        self.transaction_fee = 0.50  # Flat commission per trade to prevent micro-scalping
        
        # Environment state
        self.market = None
        self.cash = 0.0
        self.shares = 0
        self.total_invested = 0.0
        self.price_history = []
        self.current_step = 0
        self.max_steps = 100  # length of one simulation episode
        self.consecutive_holds = 0
        
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        
        self.market = Market()
        self.cash = self.initial_cash
        self.shares = 0
        self.total_invested = 0.0
        self.price_history = [self.market.price]
        self.current_step = 0
        self.consecutive_holds = 0
        
        return self._get_obs(), {}
        
    def _get_obs(self):
        price = self.market.price
        
        short_trend = 0.0
        long_trend = 0.0
        if len(self.price_history) >= 3:
            short_trend = self.price_history[-1] - self.price_history[-3]
        if len(self.price_history) >= 15:
            long_trend = self.price_history[-1] - self.price_history[-15]
        elif len(self.price_history) > 1:
            long_trend = self.price_history[-1] - self.price_history[0]
            
        avg_buy_price = 0.0
        if self.shares > 0:
            avg_buy_price = self.total_invested / self.shares
            
        return np.array([
            price,
            short_trend,
            long_trend,
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
        
        long_trend = 0.0
        short_trend = 0.0
        if len(self.price_history) >= 15:
            long_trend = self.price_history[-1] - self.price_history[-15]
        if len(self.price_history) >= 3:
            short_trend = self.price_history[-1] - self.price_history[-3]
        
        # Execute the chosen action
        # 0 = HOLD, 1 = BUY, 2 = SELL
        trade_executed = False
        
        if action == 1: # BUY
            if self.cash >= (price + self.transaction_fee):
                self.shares += 1
                self.cash -= (price + self.transaction_fee)
                self.total_invested += price
                trade_executed = True
        elif action == 2: # SELL
            if self.shares > 0:
                avg_price = self.total_invested / self.shares
                self.shares -= 1
                self.cash += (price - self.transaction_fee)
                self.total_invested -= avg_price
                trade_executed = True

        # User mandate: Treat invalid actions exactly like Holds to prevent looping loopholes
        if not trade_executed:
            self.consecutive_holds += 1
        else:
            self.consecutive_holds = 0
                
        # Calculate new net worth
        current_net_worth = self.cash + (self.shares * price)
        
        # Base reward is the natural change in net worth
        reward = current_net_worth - prev_net_worth
        
        # We completely remove all artificial penalties for invalid actions to 
        # prevent the network from hiding in the 100% HOLD safe state.
            
        # Enforce valid actions so it learns what the buttons do
        if action != 0 and not trade_executed:
            reward -= 0.5
            
        # --- BEHAVIORAL REWARD SHAPING (Architected to user's exact specifications) ---
        
        # Rule 1: "When the price is dipping buy aggressively"
        if short_trend < -0.2 and action == 1:
            reward += 3.0  # Strong reward for buying the dip!
            
        # Rule 2: "If the bot predicts the market to go up let it hold and go for bigger profits"
        if short_trend > 0.2 and self.shares > 0:
            if action == 0:
                reward += 1.0  # Good! Patiently letting profits run.
            elif action == 2:
                reward -= 2.0  # Bad! Selling too early while it's still rocketing up.
                
        # Rule 3: "If the market starts coming down it sells and books the profit"
        if short_trend < -0.2 and self.shares > 0:
            if action == 2:
                reward += 3.0  # Good! Selling before the crash wipes out the profit.
            elif action == 0:
                reward -= 2.0  # Bad! Bag-holding crashing shares.
                
        # Rule 4: "Penalty if the bot holds for 5 trades continuously"
        # We lower the penalty relative to the trade rewards so it doesn't just panic-trade blindly.
        if self.consecutive_holds >= 5:
            reward -= 2.0
            
        terminated = False
        truncated = self.current_step >= self.max_steps
        
        info = {
            "net_worth": current_net_worth,
            "cash": self.cash,
            "shares": self.shares
        }
        
        return self._get_obs(), reward, terminated, truncated, info
