import numpy as np
import pandas as pd

def compute_cumulative_returns(df, return_col):
    """Returns cumulative returns (base 1)"""
    return (df[return_col].cumsum()).apply(np.exp)

def compute_volatility(df, return_col, freq=252):
    """Returns annualized volatility"""
    return df[return_col].std() * np.sqrt(freq)

def compute_total_return(cum_returns):
    """Total return (final value - 1)"""
    return cum_returns.iloc[-1] - 1

def compute_sharpe_ratio(df, return_col, risk_free_rate=0.0, freq=252):
    """Returns the annualized Sharpe Ratio"""
    excess_ret = df[return_col] - (risk_free_rate / freq)
    return excess_ret.mean() / excess_ret.std() * np.sqrt(freq)

def compute_max_drawdown(cum_returns):
    """Returns the maximum drawdown (%)"""
    roll_max = cum_returns.cummax()
    drawdown = (cum_returns - roll_max) / roll_max
    return drawdown.min()

def summarize_performance(df):
    """
    Takes a DataFrame with the following columns:
    - 'Log Returns'
    - 'Strategy Returns'
    
    Returns a dict with performance metrics and an updated DataFrame.
    """
    df = df.copy()
    df['Cumulative Market'] = compute_cumulative_returns(df, 'Log Returns')
    df['Cumulative Strategy'] = compute_cumulative_returns(df, 'Strategy Returns')

    perf = {
        'market_return': compute_total_return(df['Cumulative Market']),
        'strategy_return': compute_total_return(df['Cumulative Strategy']),
        'market_vol': compute_volatility(df, 'Log Returns'),
        'strategy_vol': compute_volatility(df, 'Strategy Returns'),
        'market_sharpe': compute_sharpe_ratio(df, 'Log Returns'),
        'strategy_sharpe': compute_sharpe_ratio(df, 'Strategy Returns'),
        'strategy_max_dd': compute_max_drawdown(df['Cumulative Strategy']),
    }
    return df, perf
