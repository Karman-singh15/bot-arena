# 🧠 Bot Arena

A multi-agent simulation system that models how traders from different economic backgrounds behave under changing market and geopolitical conditions.

This project combines **behavioral modeling + algorithmic trading + machine learning** to simulate and analyze decision-making patterns in financial markets.

---

## 🚀 Overview

Traditional trading bots focus only on maximizing profit.

This goes further by introducing **human-like behavioral biases** based on economic background, risk tolerance, and psychological factors.

Each agent (bot):

* Has a unique personality (risk, patience, capital)
* Observes market conditions and events
* Makes Buy/Sell/Hold decisions
* Logs its reasoning process

---

## 🧩 Core Features

* 📈 **Market Simulation Engine**

  * Synthetic price generation (random walk, trends, volatility)
* 🤖 **Multi-Agent System**

  * Multiple bots with distinct economic profiles
* 🧠 **Behavioral Modeling**

  * Risk tolerance
  * Decision bias
  * Capital constraints
* 📊 **Trading Engine**

  * Buy / Sell / Hold execution
  * Portfolio tracking
* 🧾 **Decision Logging**

  * Transparent reasoning for each trade
* 🔮 **(Planned) ML Integration**

  * Predictive decision models
  * Reinforcement learning agents

---

## 🤖 Agents (Planned)

| Agent                 | Description                                |
| --------------------- | ------------------------------------------ |
| Low Income Trader     | Risk-averse, short-term survival decisions |
| Middle Class Investor | Balanced strategy, moderate risk           |
| Wealthy Investor      | Long-term holding, diversified             |
| Hedge Fund Bot        | Data-driven, aggressive                    |
| Speculator            | High-risk, high-reward behavior            |

---

## 🏗️ Project Structure

```
bot-arena/
│
├── main.py            # Entry point
├── simulation.py      # Core simulation loop
├── market.py          # Market behavior
├── bot.py             # Agent logic
├── logger.py          # Decision logging (planned)
├── config.py          # Bot configurations (planned)
```

---

## ⚙️ How It Works

1. The **market** generates price changes over time
2. Each **agent observes the market state**
3. The agent decides:

   * BUY
   * SELL
   * HOLD
4. The system executes the trade
5. Logs are generated for analysis

---

## ▶️ Running the Project

### 1. Clone the repo

```bash
git clone https://github.com/your-username/bot-arena.git
cd bot-arena
```

### 2. Run the simulation

```bash
python main.py
```

---

## 🧪 Example Output

```
Step 1 | Price: 100.23

Conservative → HOLD | Cash: 1000 | Shares: 0  
Aggressive → BUY | Cash: 899.77 | Shares: 1  
```

---

## 📅 Roadmap

### Phase 1 (Current)

* [x] Market simulation
* [x] Basic agents
* [x] Trading loop

### Phase 2

* [ ] Add 5 behavioral agents
* [ ] Portfolio tracking
* [ ] Advanced logging

### Phase 3

* [ ] Economic & geopolitical event simulation
* [ ] Dynamic agent reactions

### Phase 4

* [ ] Machine Learning integration
* [ ] Decision prediction models

### Phase 5

* [ ] Web dashboard (Next.js)
* [ ] Real-time visualization
* [ ] User interaction with agents

---

## 🧠 Tech Stack

* Python (Core simulation)
* NumPy / Pandas (planned)
* FastAPI (planned backend API)
* Next.js + TailwindCSS (planned frontend)
* ML Models (Scikit-learn / RL)

---

## 🎯 Goals of the Project

* Explore how **economic background affects trading behavior**
* Simulate **real-world decision-making under uncertainty**
* Build a **scalable ML-powered trading system**
* Strengthen skills in:

  * Machine Learning
  * System Design
  * Simulation Modeling

---

## 📌 Future Ideas

* News sentiment analysis
* Multi-asset trading (crypto, stocks, forex)
* Reinforcement learning agents
* User vs bot trading mode

---

## 🤝 Contributing

This is a personal learning + research project, but contributions and ideas are welcome.

---

## 📜 License

MIT License

---

## 💡 Author

Built by Karman
Aspiring ML Engineer 🚀
