import streamlit as st

st.set_page_config(
    page_title="Quant Backtest Dashboard",
    layout="wide",
    page_icon="📈"
)

st.title("📊 Quantitative Strategy Backtesting Dashboard")

st.markdown("""
Welcome to the **Quant Backtest Dashboard**!  
This interactive platform lets you explore and compare quantitative trading strategies based on historical market data.

### 📌 Available Strategies
Use the sidebar to navigate between:
- **Moving Average Crossover**
- **Mean Reversion**

### 📈 Each strategy page includes:
- A customizable strategy configuration panel
- Interactive performance visualizations
- Executed buy/sell signals
- Key portfolio statistics (Sharpe ratio, drawdown, total return, etc.)

---

This dashboard is ideal for:
- Testing trading ideas with real data
- Understanding how different strategies behave
- Comparing their performance under various market conditions

Feel free to tweak the parameters and see how strategies react in different scenarios.
""")
