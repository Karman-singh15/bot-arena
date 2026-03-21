from market import Market
from bot import Bot

class Simulation:
    def __init__(self):
        self.market = Market()

        self.bots = [
            Bot("Conservative", 1000, 0.2),
            Bot("Aggressive", 1000, 0.8)
        ]
        self.trade_logs = {bot.name: [] for bot in self.bots}

    def run(self, steps=50):
        for step in range(steps):
            price = self.market.step()
            print(f"\nStep {step} | Price: {price:.2f}")

            for bot in self.bots:
                initial_shares = bot.shares
                action = bot.decide(price)
                bot.act(action, price)
                
                if bot.shares > initial_shares:
                    self.trade_logs[bot.name].append(f"Bought at Step {step} | Price: {price:.2f}")
                elif bot.shares < initial_shares:
                    self.trade_logs[bot.name].append(f"Sold at Step {step} | Price: {price:.2f}")

                info = f"{bot.name} → {action} | Cash: {bot.cash:.2f} | Shares: {bot.shares}"
                if len(bot.price_history) >= 5:
                    info += f" | Trend: {bot.current_trend:+.2f} | Buy: <{bot.current_buy_threshold:.2f} | Sell: >{bot.current_sell_threshold:.2f}"
                print(info)

        print("\n--- Final Results ---")
        for bot in self.bots:
            print(f"{bot.name} → Final Value: {bot.cash + bot.shares * self.market.price:.2f}")
            
        print("\n--- Trade Analysis ---")
        for bot in self.bots:
            print(f"\n{bot.name} Trades:")
            if not self.trade_logs[bot.name]:
                print("  No trades made.")
            else:
                for log in self.trade_logs[bot.name]:
                    print(f"  {log}")