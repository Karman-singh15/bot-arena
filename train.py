import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from rl_env import TradingEnv
import os

def main():
    print("Initializing Market Environment...")
    env = TradingEnv(initial_cash=1000.0, risk_tolerance=0.8)
    
    # Check if the environment follows the Gymnasium API
    try:
        check_env(env, warn=True)
        print("Environment verified!")
    except Exception as e:
        print(f"Environment check failed: {e}")
        return
        
    print("Setting up PPO RL Agent...")
    if os.path.exists("ppo_trading_bot.zip"):
        print("Loading existing model...")
        model = PPO.load("ppo_trading_bot", env=env)
    else:
        print("Creating new model...")
        model = PPO("MlpPolicy", env, verbose=1, learning_rate=0.0003)
    
    print("Training the agent for 50,000 timesteps... (This may take a minute)")
    model.learn(total_timesteps=100000)
    
    print("Training complete! Saving model to 'ppo_trading_bot'...")
    model.save("ppo_trading_bot")
    
    # Evaluate the trained agent
    print("\n--- Evaluating Trained Agent ---")
    obs, info = env.reset()
    
    for i in range(100):
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        
        action_name = ["HOLD", "BUY", "SELL"][action]
        price = obs[0]
        print(f"Step {i:02d} | Price: ${price:.2f} | Action: {action_name} | Net Worth: ${info['net_worth']:.2f}")
        
        if terminated or truncated:
            break

if __name__ == "__main__":
    main()
