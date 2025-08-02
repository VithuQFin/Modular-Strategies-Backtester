import pandas as pd
from strategies.moving_average import MovingAverageCrossStrategy
from strategies.mean_reversion import MeanReversionStrategy
from backtester.engine import BacktestEngine
from backtester.reporting import generate_report
from data.data_loader import fetch_multiple_tickers
from data.data_cleaning import clean_data_files

def load_data(ticker, start, end, raw_path="data/raw/", clean_path="data/clean/"):
    """
    Loads and cleans data for a given ticker and time period.

    :param ticker: str - Ticker symbol
    :param start: datetime - Start date
    :param end: datetime - End date
    :param raw_path: str - Directory for raw data
    :param clean_path: str - Directory for cleaned data
    :return: DataFrame - Cleaned historical price data
    """
    fetch_multiple_tickers([ticker], start, end, raw_path=raw_path)
    clean_data_files()

    start_str = start.strftime("%Y%m%d")
    end_str = end.strftime("%Y%m%d")
    file_path = f"{clean_path}/{ticker}_{start_str}_to_{end_str}.csv"
    try:
        data = pd.read_csv(file_path, parse_dates=['Date'])
        if 'Adj Close' not in data.columns or 'Date' not in data.columns:
            raise ValueError(f"'Date' and 'Adj Close' columns are required in {file_path}")
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_path} not found. Please check clean_data_files.")

def run_backtest(strategy_class, data, params, initial_cash):
    """
    Runs a backtest for a given strategy.

    :param strategy_class: class - Strategy class (e.g., MovingAverageCrossStrategy)
    :param data: DataFrame - Historical data
    :param params: dict - Strategy parameters
    :param initial_cash: float - Starting capital
    :return: BacktestEngine - Engine instance after execution
    """
    strategy = strategy_class(data, **params)
    engine = BacktestEngine(strategy, data, initial_cash)
    engine.run()
    return engine

def main():
    # Strategy configurations
    strategies = [
        {
            "name": "Moving Average",
            "class": MovingAverageCrossStrategy,
            "ticker": "AAPL",
            "start": pd.to_datetime("2010-01-01"),
            "end": pd.to_datetime("2018-06-29"),
            "params": {"short_window": 42, "long_window": 252}
        },
        {
            "name": "Mean Reversion",
            "class": MeanReversionStrategy,
            "ticker": "AAPL",
            "start": pd.to_datetime("2022-01-01"),
            "end": pd.to_datetime("2024-12-31"),
            "params": {"window": 20, "threshold": 2.0}
        }
    ]

    initial_cash = 100000
    raw_path = "data/raw/"
    clean_path = "data/clean/"

    # Run each strategy
    for config in strategies:
        print(f"\n🚀 Running strategy: {config['name']} ({config['ticker']})")
        try:
            # Load and clean data
            data = load_data(config['ticker'], config['start'], config['end'], raw_path, clean_path)

            # Run backtest
            engine = run_backtest(
                config['class'],
                data,
                config['params'],
                initial_cash
            )

            # Generate report
            generate_report(
                engine,
                config['class'](data, **config['params']),
                *config['params'].values(),
                initial_cash=initial_cash
            )

        except Exception as e:
            print(f"❌ Error for {config['name']} ({config['ticker']}): {e}")

if __name__ == "__main__":
    main()
