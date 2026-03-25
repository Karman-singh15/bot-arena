# test_rl.py

from stable_baselines3 import PPO
from rl_env import TradingEnv

def main():
    print("📦 Loading trained model...")

    # Load model
    model = PPO.load("models/ppo_trading_bot")

    # Create environment
    env = TradingEnv(initial_cash=5000.0, risk_tolerance=0.8)

    obs, info = env.reset()

    print("\n🚀 Starting Evaluation...\n")

    for step in range(500):
        # Predict action
        action, _ = model.predict(obs, deterministic=True)

        # Take step
        obs, reward, terminated, truncated, info = env.step(action)

        action_name = ["HOLD", "BUY", "SELL"][action]
        price = obs[0]
        net_worth = info.get("net_worth", 0)

        print(
            f"Step {step:03d} | Price: {price:.2f} | Action: {action_name} | Net Worth: {net_worth:.2f} | short trend: {obs[1]:.2f} | long trend: {obs[2]:.2f}"
        )

        if terminated or truncated:
            break

    print(f"\n💰 Final Net Worth: {net_worth:.2f}")
    print("Shares: ",obs[4])
    print("✅ Evaluation complete!")

if __name__ == "__main__":
    main()