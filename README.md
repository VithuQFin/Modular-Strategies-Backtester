# Simple Modular Strategy Backtester

This project is a modular backtesting engine for evaluating trading strategies such as **Moving Average Crossover** and **Mean Reversion**. It allows users to simulate trades, measure performance, and generate detailed analytics using historical data.

## Project Structure

```plaintext
.
├── backtester/ # Core backtest engine and metrics
│ ├── engine.py # Executes the trading logic
│ ├── metrics.py # Performance metrics (Sharpe, drawdown, etc.)
│ ├── order.py # Trade order representation
│ ├── portfolio.py # Cash & position tracking
│ └── reporting.py # Report generation (graph + stats)
│
├── data/ # Data ingestion and cleaning
│ ├── raw/ # Raw CSV files from Yahoo Finance
│ ├── clean/ # Cleaned and preprocessed files
│ ├── data_cleaning.py # Cleans raw data
│ └── data_loader.py # Downloads historical stock data
│
├── strategies/ # Trading strategy logic
│ ├── moving_average.py # Moving Average Crossover strategy
│ └── mean_reversion.py # Mean Reversion strategy
│
├── pages/ # [Ignored] Streamlit interface pages
├── utils/ # (Reserved for future utilities)
├── main.py # CLI execution of strategies
└── Home.py # [Ignored] Streamlit landing page
```

---

>`pages/` and `Home.py` are ignored via `.gitignore` as they are specific to the Streamlit frontend.

---

## Features

- Clean, modular Python architecture
- Built-in strategies:
  - Moving Average Crossover
  - Mean Reversion (Z-score)
- Performance analytics:
  - Cumulative returns
  - Sharpe Ratio
  - Maximum Drawdown
  - Portfolio value evolution
- Automatic data fetching and cleaning (Yahoo Finance)
- Interactive dashboard with **Streamlit** (optional)

---

## Requirements

Install dependencies:

```plaintext
pip install -r requirements.txt
```

Or manually install:

```plaintext
pip install pandas numpy matplotlib yfinance plotly streamlit
```

How to Use
1. Run the CLI Backtest

```plaintext
python main.py
```

This will execute the predefined strategies and output performance stats and plots.

---

## Strategy Overview

Mean Reversion

    Based on z-score of price relative to a moving average

    Buy when price is significantly below average (undervalued)

    Sell when price is significantly above average (overvalued)

Moving Average Crossover

    Long when short MA > long MA

    Exit when short MA < long MA

Sample Output

    Orders executed: 📋 BUY/SELL logs

    Portfolio value curve: 💰 over time

    Strategy vs Market return: 📈

    Risk metrics: ✅ Sharpe, volatility, drawdown
