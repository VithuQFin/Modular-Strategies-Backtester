import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from backtester.metrics import summarize_performance

def generate_report(engine, strategy, *strategy_params, initial_cash):
    df = strategy.generate_signals()

    # Add required columns
    df['Log Returns'] = np.log(df['Adj Close'] / df['Adj Close'].shift(1))
    df['Signal'] = df['signal'].shift(1)  # Shift to avoid lookahead bias
    df['Strategy Returns'] = df['Signal'] * df['Log Returns']
    df.dropna(inplace=True)

    # Compute performance metrics
    df, perf = summarize_performance(df)

    # 🔹 Display executed orders
    print("\n📋 EXECUTED ORDERS:")
    for order in engine.orders:
        print(order)

    # 🔹 Plot price chart and strategy indicators if available
    plt.figure(figsize=(16, 9))
    plt.plot(df['Date'], df['Adj Close'], label='Adjusted Price')

    if 'short_ma' in df.columns and 'long_ma' in df.columns:
        short_window = strategy_params[0]
        long_window = strategy_params[1]
        plt.plot(df['Date'], df['short_ma'], label=f'Short MA ({short_window})')
        plt.plot(df['Date'], df['long_ma'], label=f'Long MA ({long_window})')

    elif 'mean' in df.columns and 'zscore' in df.columns:
        window = strategy_params[0]
        plt.plot(df['Date'], df['mean'], label=f'Moving Average ({window})')

    # Buy/Sell signals
    buy_signals = [o for o in engine.orders if o.order_type == 'buy']
    sell_signals = [o for o in engine.orders if o.order_type == 'sell']

    plt.scatter([o.date for o in buy_signals], [o.price for o in buy_signals],
                marker='^', color='green', label='BUY', s=100)
    plt.scatter([o.date for o in sell_signals], [o.price for o in sell_signals],
                marker='v', color='red', label='SELL', s=100)

    plt.title(f"📈 Backtest: {getattr(strategy, 'name', 'Strategy')}")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # 🔹 Cumulative performance
    plt.figure(figsize=(16, 8))
    plt.plot(df['Date'], df['Cumulative Market'], label='Buy & Hold')
    plt.plot(df['Date'], df['Cumulative Strategy'], label='Strategy')
    plt.title("📊 Cumulative Performance")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Value (base 1)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # 🔹 Actual portfolio value over time
    portfolio_df = pd.DataFrame(engine.portfolio.history, columns=['Date', 'Action', 'Price', 'Position', 'Cash'])
    portfolio_df['Date'] = pd.to_datetime(portfolio_df['Date'])
    portfolio_df.sort_values(by='Date', inplace=True)
    portfolio_df['Portfolio Value'] = portfolio_df['Cash'] + portfolio_df['Position'] * portfolio_df['Price']

    last_price = df['Adj Close'].iloc[-1]
    final_value = engine.portfolio.cash + engine.portfolio.position * last_price
    total_return = (final_value / initial_cash - 1) * 100

    # 🔹 Performance Summary
    print("\n📊 PERFORMANCE SUMMARY:")
    print(f"➡️ Market Total Return: {perf['market_return'] * 100:.2f}%")
    print(f"➡️ Strategy Total Return: {perf['strategy_return'] * 100:.2f}%")
    print(f"📈 Market Volatility (ann.): {perf['market_vol']:.2%}")
    print(f"📉 Strategy Volatility (ann.): {perf['strategy_vol']:.2%}")
    print(f"📏 Market Sharpe Ratio: {perf['market_sharpe']:.2f}")
    print(f"📏 Strategy Sharpe Ratio: {perf['strategy_sharpe']:.2f}")
    print(f"📉 Strategy Max Drawdown: {perf['strategy_max_dd'] * 100:.2f}%")

    print("\n💼 FINAL PORTFOLIO STATE:")
    print(f"💵 Remaining Cash       : {engine.portfolio.cash:.2f} $")
    print(f"📦 Remaining Position   : {engine.portfolio.position:.4f} units")
    print(f"📈 Closing Price        : {last_price:.2f} $")
    print(f"💰 Final Portfolio Value: {final_value:.2f} $")
    print(f"📊 Actual Portfolio Return: {total_return:.2f} %")

    print("\n📊 Return Comparison:")
    print(f"- Strategy (simulated log-return, base 1): {(perf['strategy_return']) * 100:.2f} %")
    print(f"- Real Portfolio Return                 : {total_return:.2f} %")

    # 🔹 Plot actual portfolio value
    plt.figure(figsize=(16, 8))
    plt.plot(portfolio_df['Date'], portfolio_df['Portfolio Value'], label='Actual Portfolio Value', color='purple')
    plt.title("📈 Portfolio Value Over Time")
    plt.xlabel("Date")
    plt.ylabel("Value ($)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def generate_report_for_streamlit(engine, strategy, *strategy_params, initial_cash):
    df = strategy.generate_signals()
    df['Log Returns'] = np.log(df['Adj Close'] / df['Adj Close'].shift(1))
    df['Signal'] = df['signal'].shift(1)
    df['Strategy Returns'] = df['Signal'] * df['Log Returns']
    df.dropna(inplace=True)

    df, perf = summarize_performance(df)

    # Compute portfolio value
    portfolio_df = pd.DataFrame(engine.portfolio.history, columns=['Date', 'Action', 'Price', 'Position', 'Cash'])
    portfolio_df['Date'] = pd.to_datetime(portfolio_df['Date'])
    portfolio_df.sort_values(by='Date', inplace=True)
    portfolio_df['Portfolio Value'] = portfolio_df['Cash'] + portfolio_df['Position'] * portfolio_df['Price']

    last_price = df['Adj Close'].iloc[-1]
    final_value = engine.portfolio.cash + engine.portfolio.position * last_price
    total_return = (final_value / initial_cash - 1) * 100

    report = {
        "df": df,
        "perf": perf,
        "orders": engine.orders,
        "portfolio": portfolio_df,
        "final_value": final_value,
        "total_return": total_return,
        "last_price": last_price,
        "params": strategy_params
    }

    return report
