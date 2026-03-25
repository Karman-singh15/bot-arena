# train_rl.py

import os
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.callbacks import EvalCallback
from rl_env import TradingEnv

MODEL_PATH = "models/ppo_trading_bot"
LOG_PATH = "logs/"

def make_env():
    return TradingEnv(initial_cash=1000.0, risk_tolerance=0.8)

def main():
    print("🚀 Starting RL Training Pipeline...")

    # Create folders if not exist
    os.makedirs("models", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    # Wrap environment
    env = DummyVecEnv([make_env])

    # Load existing model or create new
    if os.path.exists(MODEL_PATH + ".zip"):
        print("📦 Loading existing model...")
        model = PPO.load(MODEL_PATH, env=env, ent_coef=0.05)  # Override exploration noise
    else:
        print("🧠 Creating new model...")
        model = PPO(
            "MlpPolicy",
            env,
            verbose=1,
            learning_rate=3e-4,
            batch_size=64,
            gamma=0.99,
            ent_coef=0.05,  # Increased entropy coefficient for higher exploration noise
            tensorboard_log=LOG_PATH
        )

    # Evaluation environment
    eval_env = DummyVecEnv([make_env])

    eval_callback = EvalCallback(
        eval_env,
        best_model_save_path="./models/best/",
        log_path="./logs/",
        eval_freq=5000,
        deterministic=True,
        render=False
    )

    print("🏋️ Training started...")
    model.learn(
        total_timesteps=200_000,
        callback=eval_callback,
        progress_bar=True
    )

    print("💾 Saving model...")
    model.save(MODEL_PATH)

    print("✅ Training complete!")

if __name__ == "__main__":
    main()