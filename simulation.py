from market import Market
from bot import Bot

class Simulation:
    def __init__(self):
        self.market = Market()

        self.bots = [
            Bot("Conservative", 1000, 0.2),
            Bot("Aggressive", 1000, 0.8)
        ]

    def run(self, steps=50):
        for step in range(steps):
            price = self.market.step()
            print(f"\nStep {step} | Price: {price:.2f}")

            for bot in self.bots:
                action = bot.decide(price)
                bot.act(action, price)

                print(
                    f"{bot.name} → {action} | Cash: {bot.cash:.2f} | Shares: {bot.shares}"
                )

        print("\n--- Final Results ---")
        for bot in self.bots:
            print(f"{bot.name} → Final Value: {bot.cash + bot.shares * self.market.price:.2f}")